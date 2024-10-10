import datetime
from datetime import timedelta
import time
from argparse import Namespace
from typing import Tuple
import json
from pathlib import Path
import subprocess

import requests
import sched

from automate import automateLogin
from book_court import book_courts, prepare_book_data
from captcha import preload_model
from prefs import get_available_target_courts
from config import (
    format_book_header,
    format_captcha_header,
)
import globals
from arguments import parse_args, Args
from utils import log, get_time_diff


def prepare_data(prefSession: requests.Session, args: Namespace):
    '''
    Prepare a whole lot of data, save to `globals`. Preparation includes
    - Captcha recognizer
    - Login
    - Checking for available courts
    '''
    globals.target_date = str(datetime.date.today() + timedelta(days=args.days_from_now))
    log(f"Target date: {globals.target_date}")
    globals.infer_device = "cpu"
    globals.captcha_recognizer = preload_model(globals.infer_device)
    globals.payment_method = args.paymentmethod
    globals.studentid = args.studentid
    globals.password = args.password
    globals.phone = args.phone

    globals.session = requests.Session()

    log("Getting prefs...")
    prefs = get_available_target_courts(
        prefSession,
        target_gym_name=args.gym,
        fields=args.fields,
        accept_free_courts=args.accept_free_courts,
    )
    globals.target_court_costs = prefs["costs"]
    globals.target_court_infos = prefs["infos"]
    globals.target_court_tokens = prefs["tokens"]
    globals.target_court_ids = prefs["ids"]
    log(f"Found available target courts: {prefs['infos']}")

    if len(prefs['infos']) == 0:
        log("No available courts are available... exiting.")
        exit()

    log("Logging in...")
    login_result = automateLogin(
        globals.studentid,
        globals.password,
        globals.target_gym_id,
        globals.target_gym_item_id,
        # args.headless,
    )
    globals.serverid = login_result["serverid"]
    globals.jsessionid = login_result["jsessionid"]
    globals.username = login_result["username"]
    globals.chrome_driver = login_result["driver"]
    log(f"You are logged in as {globals.username}")

    globals.book_headers = format_book_header(
        globals.serverid,
        globals.jsessionid,
        globals.target_gym_id,
        globals.target_gym_item_id,
        globals.target_date,
    )
    globals.captcha_headers = format_captcha_header(
        globals.serverid,
        globals.jsessionid,
        globals.target_gym_id,
        globals.target_gym_item_id,
        globals.target_date,
    )
    if (
        globals.target_court_ids
        and globals.target_court_costs
        and globals.target_court_infos
        and globals.target_court_tokens
    ):
        log(
            f"Acquired necessary resources for Gym: {globals.target_gym_name_zh} on Date: {globals.target_date}"
        )


def calibrate_local_time():
    globals.time_difference = get_time_diff()


def prepare_time(
    book_time: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime, datetime.datetime]:
    actual_book_time = book_time - timedelta(microseconds=60000)
    update_data_time = book_time - timedelta(seconds=10)
    calib_time = update_data_time + timedelta(seconds=5)
    return actual_book_time, update_data_time, calib_time


def get_book_time(booknow: bool) -> datetime.datetime:
    '''
    Get the time that we will do the booking.
    '''
    now = datetime.datetime.now()
    if booknow:
        # For testing purposes
        book_time = now + timedelta(seconds=12)
        return book_time

    if now.hour > 8:
        # Reserve tomorrow morning
        target_date = now.date() + timedelta(days=1)
    else:
        target_date = now.date()

    book_time = datetime.datetime.combine(target_date, datetime.time(8, 0, 0, 0))
    return book_time


def book_main(args):
    log("Initialized the script.")
    print(json.dumps(vars(args), indent=4))
    court_fetcher_session = requests.Session()
    scheduler = sched.scheduler(time.time, time.sleep)

    book_time = get_book_time(booknow=args.booknow)
    actual_book_time, prepare_data_time, calib_time = prepare_time(book_time)
    log(f"Scheduled book time is set to {book_time}.")
    log(f"Optimized book time is set to {actual_book_time}.")
    log(f"Data preparation time is set to {prepare_data_time}.")
    log(f"Calibration time is set to {calib_time}.")
    timestamp_recalibration = (
        time.mktime(calib_time.timetuple()) + calib_time.microsecond / 1e6
    )
    scheduler.enterabs(timestamp_recalibration, 1, calibrate_local_time)

    scheduler.enterabs(
        time.mktime(prepare_data_time.timetuple()) + prepare_data_time.microsecond / 1e6,
        1,
        prepare_data,
        argument=(court_fetcher_session, args),
    )
    scheduler.enterabs(
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
                time.mktime(target_time_3.timetuple()) + target_time_3.microsecond / 1e6
            )
            log(f"Book time is set to {target_time_3}.")
            scheduler.enterabs(timestamp_3, 1, book_courts)
            calibration_done = True

        scheduler.run(blocking=False)
        time.sleep(0.02)


def spawn_multiple_users(args: Args):
    """
    When multiple users are specified, this function will spawn multiple
    processes to book courts for each user.
    """
    assert isinstance(args.studentid, list)
    assert isinstance(args.phone, list)
    assert isinstance(args.password, list)
    assert args.fields is not None

    fields = args.fields
    n_users = len(args.studentid)
    n_fields = len(fields)
    n_per_user = n_fields // n_users

    for i in range(n_users):
        """
        Rolling fields, to ensure that this user will also try to book
        other fields when its targets are unavailable.
        In other words, if the specified fields are: [1, 2, 3, 4, 5, 6, 7],
        and there are 2 users, then the --fields argument for them are:
        - User 1: [1, 2, 3, 4, 5, 6, 7]
        - User 2: [4, 5, 6, 7, 1, 2, 3]
        This means that User 2 will prioritize courts 4, 5, 6, 7, but will
        also try to book courts 1, 2, 3 if courts 4, 5, 6, 7 are unavailable.
        """
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
    default_args_path = Path('args.json')
    credentials_path = Path('credentials.json')
    default_args = json.load(open(default_args_path, 'r', encoding='utf8'))
    credentials = json.load(open(credentials_path, 'r', encoding='utf8'))

    default_args.update(credentials)

    cmd_args = parse_args()
    args = Args(**vars(cmd_args))

    # Set all `None` arguments to the default arguments.
    for k, v in default_args.items():
        if getattr(args, k) is None:
            setattr(args, k, v)

    print(vars(args))
    # if args.booknow:
    #     args.gym = "Tennis"
    #     args.paymentmethod = 1

    if isinstance(args.studentid, list) and len(args.studentid) == 1:
        assert isinstance(args.password, list)
        assert isinstance(args.phone, list)
        # If only one user is specified, only book courts for this user.
        args.studentid = args.studentid[0]
        args.password = args.password[0]
        args.phone = args.phone[0]

    if isinstance(args.studentid, int):
        book_main(args)
    else:
        spawn_multiple_users(args)
