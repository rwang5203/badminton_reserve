import json
import datetime
import random
import re
import sys
import time
from typing import Tuple

import numpy as np
import cv2
import torch
from torchvision.transforms import ToTensor

from automate import automatePay
from availability_check import availability_update
import globals
import config
from predict import predict_captcha
from utils import log


def book_courts():
    """
    Reserve courts with preferences, with updated resources.
    """
    book_resp = globals.session.post(
        config.book_url,
        data=globals.book_data,
        headers=globals.book_headers,
        verify=False,
    )  # noqa
    log(
        f"Booking {globals.index+1}/{len(globals.prefCourtTokens)}: 【{globals.prefGymNameCN} {globals.book_date} {globals.prefCourtInfos[globals.index % len(globals.prefCourtTokens)]}】..."  # noqa
    )  # noqa
    if "预定成功" in json.loads(book_resp.text)["msg"]:
        log(
            f"Booked: {globals.prefGymNameCN} {globals.book_date} {globals.prefCourtInfos[globals.index % len(globals.prefCourtTokens)]}"  # noqa
        )  # noqa
        automatePay(
            globals.chromeDriver,
            globals.session,
            globals.serverid,
            globals.jsessionid,
            globals.payment_method,
        )
        sys.exit(1)
    else:
        print(json.loads(book_resp.text)["msg"])
        time.sleep(0.72)
        prepare_book_data()
        availability_update()
    success_count = 0
    success_court_infos = []
    book_count = 0
    update_lapse = 0

    while globals.prefCourtTokens and book_count < 12 and success_count < 1:
        if book_count > 0:
            start_time = time.time()
            prepare_book_data()
            availability_update()

            end_time = time.time()
            update_lapse = end_time - start_time

        book_resp = globals.session.post(
            config.book_url,
            data=globals.book_data,
            headers=globals.book_headers,
            verify=False,
        )

        log(
            f"Booking {globals.index+1}/{len(globals.prefCourtTokens)}: 【{globals.prefGymNameCN} {globals.book_date} {globals.prefCourtInfos[globals.index % len(globals.prefCourtTokens)]}】..."  # noqa
        )
        if book_resp.status_code == 200:
            book_result = json.loads(book_resp.text)["msg"]
            log(f"Returned result: {book_result}")
            if "预定成功" in book_result:
                success_count += 1
                success_court_infos.append(
                    globals.prefGymNameCN
                    + " "
                    + globals.book_date
                    + " "
                    + globals.prefCourtInfos[
                        globals.index % len(globals.prefCourtTokens)
                    ]
                )
            elif "超过预定场地数量限额" in book_result:
                break
            elif "系统检测到当前为非人工操作" in book_result:
                lock_time = int(re.search(r"已被锁定(\d+)秒", book_result).group(1))
                time.sleep(lock_time)
        else:
            log("Book server error prevented the request.")
        sleep_time = random.uniform(
            1.021 - update_lapse, 1.0211 - update_lapse
        )
        time.sleep(sleep_time)
        book_count += 1
    log(f"Book session is completed, {success_count} court(s) were booked:")
    if success_court_infos:
        for globals.index in range(len(success_court_infos)):
            log(
                f"[No. {globals.index+1}] 【{success_court_infos[globals.index]}】"
            )
        automatePay(
            globals.chromeDriver,
            globals.session,
            globals.serverid,
            globals.jsessionid,
            globals.payment_method,
        )
    sys.exit(1)


def read_image_bytes(
    buf, transform=ToTensor()
) -> Tuple[np.ndarray, torch.Tensor]:
    np_buf = np.frombuffer(buf, dtype=np.uint8)
    gray_image = cv2.imdecode(np_buf, cv2.IMREAD_GRAYSCALE)
    image = np.reshape(gray_image, (50, 200, 1))
    img_tensor = transform(image)
    return gray_image, img_tensor


def save_captcha(image, captcha_label):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"./captcha/{current_time}_{captcha_label}.jpg"
    cv2.imwrite(filename, image)


def prepare_book_data():
    captcha = globals.session.get(
        config.captcha_url, headers=globals.captcha_headers, verify=False
    )
    captcha_img, captcha_tensor = read_image_bytes(captcha.content)
    globals.captcha_label = predict_captcha(
        globals.cuda_device, captcha_tensor, globals.recognition_model
    )
    globals.book_data = config.format_book_data(
        globals.prefCourtCosts,
        globals.index,
        globals.prefCourtTokens,
        globals.phone_number,
        globals.prefGymID,
        globals.prefItemID,
        globals.book_date,
        globals.captcha_label,
        globals.payment_method,
    )
    log("Finished preparing book globals.")
