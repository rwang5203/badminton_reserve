import datetime


def log(*args, **kwargs):
    cur_time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{cur_time}] ", end='')
    print(*args, **kwargs)
