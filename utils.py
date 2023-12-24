import datetime
import ntplib


NTP_SERVER = "ntp.tuna.tsinghua.edu.cn"


def log(msg: str):
    print(
        "[" + datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3] + "] " + msg
    )


def get_time_diff():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(NTP_SERVER, version=4)
    ntp_time = datetime.datetime.utcfromtimestamp(response.tx_time)
    local_time = datetime.datetime.utcnow()
    time_difference = local_time - ntp_time
    log(f"Time difference (ms): {time_difference.total_seconds() * 1e3}")
    return time_difference.total_seconds() * 1e6


if __name__ == "__main__":
    get_time_diff()
