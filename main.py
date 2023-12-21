import datetime
from datetime import timedelta
import requests
import sched
import time
from typing import Tuple

from automate import automateLogin
from book_court import book_courts, prepare_book_data
from calibrate import time_calibration
from predict import preload_model
from prefs import get_prefs
from config import (
    format_book_header,
    format_captcha_header,
)
import globals
from args import parse_args
from utils import log


def update_data(prefSession, args):
    globals.book_date = str(datetime.date.today() + timedelta(days=3))
    globals.cuda_device = "cpu"
    globals.recognition_model = preload_model(globals.cuda_device)
    globals.payment_method = args.paymentmethod
    globals.studentid = args.studentid
    globals.password = args.password
    globals.phone_number = args.phone

    globals.session = requests.Session()

    get_prefs(prefSession, args)
    (
        globals.serverid,
        globals.jsessionid,
        globals.userName,
        globals.chromeDriver,
    ) = automateLogin(
        globals.studentid,
        globals.password,
        globals.prefGymID,
        globals.prefItemID,
        args.headless,
    )
    log(f"You are logged in as {globals.userName}")
    globals.book_headers = format_book_header(
        globals.serverid,
        globals.jsessionid,
        globals.prefGymID,
        globals.prefItemID,
        globals.book_date,
    )
    globals.captcha_headers = format_captcha_header(
        globals.serverid,
        globals.jsessionid,
        globals.prefGymID,
        globals.prefItemID,
        globals.book_date,
    )
    if (
        globals.prefCourtIDs
        and globals.prefCourtCosts
        and globals.prefCourtInfos
        and globals.prefCourtTokens
    ):
        log(
            f"Acquired necessary resources for Gym: {globals.prefGymNameCN} on Date: {globals.book_date}"
        )


def recalibrate_time():
    globals.time_difference = time_calibration()


def get_preparation_time(
    book_time: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime, datetime.datetime]:
    actual_book_time = book_time - timedelta(microseconds=50000)
    update_data_time = book_time - timedelta(seconds=10)
    calib_time = update_data_time + timedelta(seconds=5)
    return actual_book_time, update_data_time, calib_time


def get_book_time(args):
    now = datetime.datetime.now()
    if args.booknow:
        # For testing purposes
        book_time = now + timedelta(seconds=12)
        return book_time

    if now.hour > 8:
        # Reserve for tomorrow
        target_date = now.date() + timedelta(days=1)
    else:
        target_date = now.date()

    if args.booknow:
        target_date = now.date()
    book_time = datetime.datetime.combine(
        target_date, datetime.time(8, 0, 0, 0)
    )
    return book_time


def book_main(args):
    log("Initialized the script.")
    prefSession = requests.Session()
    s = sched.scheduler(time.time, time.sleep)

    book_time = get_book_time(args)
    actual_book_time, update_data_time, calib_time = get_preparation_time(
        book_time
    )
    log(f"Book time is set to {book_time}")
    log(f"Actual book time is set to {actual_book_time}")
    log(f"Update data time is set to {update_data_time}")
    log(f"Calibration time is set to {calib_time}")
    timestamp_recalibration = (
        time.mktime(calib_time.timetuple()) + calib_time.microsecond / 1e6
    )
    s.enterabs(timestamp_recalibration, 1, recalibrate_time)

    s.enterabs(
        time.mktime(update_data_time.timetuple())
        + update_data_time.microsecond / 1e6,
        1,
        update_data,
        argument=(prefSession, args),
    )
    s.enterabs(
        time.mktime(calib_time.timetuple()) + calib_time.microsecond / 1e6,
        1,
        prepare_book_data,
    )

    calibration_done = False
    
    while True:
        if not calibration_done and globals.time_difference is not None:
            time_adjustment = datetime.timedelta(
                microseconds=abs(globals.time_difference)
            )
            if globals.time_difference > 0:
                target_time_3 = book_time + time_adjustment
            else:
                target_time_3 = book_time - time_adjustment
            log("Book time calibrated.")
            timestamp_3 = (
                time.mktime(target_time_3.timetuple())
                + target_time_3.microsecond / 1e6
            )
            s.enterabs(timestamp_3, 1, book_courts)
            calibration_done = True

        s.run(blocking=False)
        time.sleep(0.02)


if __name__ == "__main__":
    args = parse_args()
    if args.booknow:
        args.gym = "Tennis"
        args.paymentmethod = 1
    print(args)
    book_main(args)
