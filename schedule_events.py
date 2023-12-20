import datetime
import requests
import sched
import time

from automate import automateLogin
from book_court import book_courts, prepare_book_data
from calibrate import time_calibration
from data import Data
from predict import preload_model
from prefs import get_prefs
from config import password, paymentmethod, phonenumber, studentid, format_book_header, format_captcha_header

from data import Data


def update_data(prefSession):
    Data.book_date = str(datetime.date.today() + datetime.timedelta(days=3))
    Data.cuda_device = "cpu"
    Data.recognition_model = preload_model(Data.cuda_device)
    Data.payment_method = paymentmethod

    Data.studentid = studentid
    Data.password = password
    Data.phone_number = phonenumber

    Data.session = requests.Session()
    
    get_prefs(prefSession)
    Data.serverid, Data.jsessionid, Data.userName, Data.chromeDriver = automateLogin(Data.studentid, Data.password, Data.prefGymID, Data.prefItemID)
    print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + f"You are logged in as {Data.userName}")
    Data.book_headers = format_book_header(Data.serverid, Data.jsessionid, Data.prefGymID, Data.prefItemID, Data.book_date)
    Data.captcha_headers = format_captcha_header(Data.serverid, Data.jsessionid, Data.prefGymID, Data.prefItemID, Data.book_date)
    if Data.prefCourtIDs and Data.prefCourtCosts and Data.prefCourtInfos and Data.prefCourtTokens:
        print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + f"Acquired necessary resources for Gym: {Data.prefGymNameCN} on Date: {Data.book_date}")
    
    
def recalibrate_time():
    Data.time_difference = time_calibration()
    
def book_main():
    print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + "Initialized the script.")
    prefSession = requests.Session()
    s = sched.scheduler(time.time, time.sleep)

    now = datetime.datetime.now()
    if now.hour > 8:
        target_date = now.date() + datetime.timedelta(days=1)  # Reserve for tomorrow
    else:
        target_date = now.date()

    target_time_1 = datetime.datetime.combine(target_date, datetime.time(7, 59, 50, 000))
    target_time_2 = datetime.datetime.combine(target_date, datetime.time(7, 59, 55, 000))

    recalibration_time = datetime.datetime.combine(target_date, datetime.time(7, 59, 59, 0))
    timestamp_recalibration = time.mktime(recalibration_time.timetuple()) + recalibration_time.microsecond / 1e6
    s.enterabs(timestamp_recalibration, 1, recalibrate_time)

    s.enterabs(time.mktime(target_time_1.timetuple()) + target_time_1.microsecond / 1e6, 1, update_data, argument=(prefSession,))
    s.enterabs(time.mktime(target_time_2.timetuple()) + target_time_2.microsecond / 1e6, 1, prepare_book_data)

    calibration_done = False
    # The third target time will be recalibrated daily
    while True:
        if not calibration_done and Data.time_difference is not None:
            # Adjust target_time_3 based on the time difference
            time_adjustment = datetime.timedelta(microseconds=abs(Data.time_difference))
            if Data.time_difference > 0:
                target_time_3 = datetime.datetime.combine(target_date, datetime.time(7, 59, 59, 950000)) + time_adjustment
            else:
                target_time_3 = datetime.datetime.combine(target_date, datetime.time(7, 59, 59, 950000)) - time_adjustment
            print("[" + datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "] " + "Book time calibrated.")
            timestamp_3 = time.mktime(target_time_3.timetuple()) + target_time_3.microsecond / 1e6
            s.enterabs(timestamp_3, 1, book_courts)
            calibration_done = True

        s.run(blocking=False)
        time.sleep(0.2)
