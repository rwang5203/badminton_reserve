import json

import cv2
import datetime
import numpy as np
import random
import re
import sys
from selenium.webdriver.common.by import By
import time
import torch
from torchvision.transforms import ToTensor

from automate import automatePay
from availability_check import availability_update
from data import Data
import config
from predict import predict_captcha

def book_courts():
    """
    Reserve courts with preferences, with updated resources.
    """
    book_resp = Data.session.post(config.book_url, data=Data.book_data, headers=Data.book_headers, verify=False)
    print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + f"Booking {Data.index+1}/{len(Data.prefCourtTokens)}: 【{Data.prefGymNameCN} {Data.book_date} {Data.prefCourtInfos[Data.index % len(Data.prefCourtTokens)]}】...")
    if "预定成功" in json.loads(book_resp.text)["msg"]:
        print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + "Booked: " + Data.prefGymNameCN + " " + Data.book_date + " " + Data.prefCourtInfos[Data.index % len(Data.prefCourtTokens)])
        automatePay(Data.chromeDriver, Data.session, Data.serverid, Data.jsessionid)
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

    while Data.prefCourtTokens and book_count < 12 and success_count < 1:
        if book_count > 0: 
            start_time = time.time()
            prepare_book_data()
            availability_update()

            end_time = time.time()
            update_lapse = end_time - start_time

        book_resp = Data.session.post(config.book_url, data=Data.book_data, headers=Data.book_headers, verify=False)

        print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + f"Booking {Data.index+1}/{len(Data.prefCourtTokens)}: 【{Data.prefGymNameCN} {Data.book_date} {Data.prefCourtInfos[Data.index % len(Data.prefCourtTokens)]}】...")
        if book_resp.status_code == 200:
            book_result = json.loads(book_resp.text)["msg"]
            print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + "Returned result: " + book_result)
            if "预定成功" in book_result:
                success_count += 1
                success_court_infos.append(Data.prefGymNameCN + " " + Data.book_date + " " + Data.prefCourtInfos[Data.index % len(Data.prefCourtTokens)])
            elif "超过预定场地数量限额" in book_result:
                break
            elif "系统检测到当前为非人工操作" in book_result:
                lock_time = int(re.search(r'已被锁定(\d+)秒', book_result).group(1))
                time.sleep(lock_time)
        else:
            print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + "Book server error prevented the request.")
        sleep_time = random.uniform(1.021 - update_lapse, 1.0211 - update_lapse)
        time.sleep(sleep_time)
        book_count += 1
    print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + f"Book session is completed, {success_count} court(s) were booked:")
    if success_court_infos:
        for Data.index in range(len(success_court_infos)):
            print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + f"[No. {Data.index+1}] 【{success_court_infos[Data.index]}】")
        automatePay(Data.chromeDriver, Data.session, Data.serverid, Data.jsessionid)
    sys.exit(1)

def read_image_bytes(buf, transform=ToTensor()) -> torch.Tensor:
    np_buf = np.frombuffer(buf, dtype=np.uint8)
    gray_image = cv2.imdecode(np_buf, cv2.IMREAD_GRAYSCALE)
    image = np.reshape(gray_image, (50, 200, 1))
    img_tensor = transform(image)
    return gray_image, img_tensor

def save_captcha(image, captcha_label):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f"./captcha/{current_time}_{captcha_label}.jpg"
    cv2.imwrite(filename, image)

def prepare_book_data():
    captcha = Data.session.get(config.captcha_url, headers = Data.captcha_headers, verify = False)
    captcha_img, captcha_tensor = read_image_bytes(captcha.content)
    Data.captcha_label = predict_captcha(Data.cuda_device, captcha_tensor, Data.recognition_model)
    Data.book_data = config.format_book_data(Data.prefCourtCosts, Data.index, Data.prefCourtTokens, Data.phone_number, Data.prefGymID, Data.prefItemID, Data.book_date, Data.captcha_label, Data.payment_method)
    print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + "Finished preparing book data.")
    