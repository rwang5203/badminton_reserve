import datetime
from datetime import timedelta
import time
from argparse import Namespace
from typing import Tuple
import json
import subprocess

import requests
import sched

from automate import automateLogin
from book_court import book_courts, prepare_book_data
from predict import preload_model
from prefs import get_prefs
from config import (
    format_book_header,
    format_captcha_header,
)
import globals
from args import parse_args
from utils import log, get_time_diff


def update_data(prefSession: requests.Session, args: Namespace):
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
        # args.headless,
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


def calibrate_local_time():
    globals.time_difference = get_time_diff()


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

    book_time = datetime.datetime.combine(
        target_date, datetime.time(8, 0, 0, 0)
    )
    return book_time


def book_main(args):
    log("Initialized the script.")
    print(json.dumps(vars(args), indent=4))
    prefSession = requests.Session()
    s = sched.scheduler(time.time, time.sleep)

    book_time = get_book_time(args)
    actual_book_time, update_data_time, calib_time = get_preparation_time(
        book_time
    )
    log(f"Scheduled book time is set to {book_time}.")
    log(f"Optimized book time is set to {actual_book_time}.")
    log(f"Data update time is set to {update_data_time}.")
    log(f"Calibration time is set to {calib_time}.")
    timestamp_recalibration = (
        time.mktime(calib_time.timetuple()) + calib_time.microsecond / 1e6
    )
    s.enterabs(timestamp_recalibration, 1, calibrate_local_time)

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


def spawn_multiple_users(args: Namespace):
    '''
    When multiple users are specified, this function will spawn multiple
    processes to book courts for each user.
    '''
    fields = args.fields
    n_users = len(args.studentid)
    n_fields = len(fields)
    n_per_user = n_fields // n_users

    for i in range(n_users):
        '''
        Rolling fields, to ensure that this user will also try to book
        other fields when its targets are unavailable.
        In other words, if the specified fields are: [1, 2, 3, 4, 5, 6, 7],
        and there are 2 users, then the --fields argument for them are:
        - User 1: [1, 2, 3, 4, 5, 6, 7]
        - User 2: [4, 5, 6, 7, 1, 2, 3]
        This means that User 2 will prioritize courts 4, 5, 6, 7, but will
        also try to book courts 1, 2, 3 if courts 4, 5, 6, 7 are unavailable.
        '''
        idx_offset = i * n_per_user
        this_fields = [fields[(i + idx_offset) % n_fields] for i in range(0, n_fields)]
        student_id = args.studentid[i]
        password = args.password[i]
        phone_number = args.phone[i]
        this_args = ["python", "main.py"]
        this_args += ["--studentid", student_id]
        this_args += ["--password", password]
        this_args += ["--phone", phone_number]
        this_args += ["--paymentmethod", str(args.paymentmethod)]
        if args.booknow:
            this_args += ["--booknow"]
        # this_args += ["--multiuser", "1"]
        this_args += ["--gym", args.gym]
        this_args += ["--fields"] + [str(x) for x in this_fields]
        print("############### Calling: ", this_args)
        subprocess.Popen(this_args)


if __name__ == "__main__":
    args = parse_args()
    # if args.booknow:
    #     args.gym = "Tennis"
    #     args.paymentmethod = 1
    if len(args.studentid) == 1:
        # If only one user is specified, only book courts for this user.
        book_main(args)
    else:
        spawn_multiple_users(args)
