import datetime


def log(msg: str):
    print(
        "[" + datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3] + "] " + msg
    )
