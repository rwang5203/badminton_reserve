import ntplib
import datetime


def time_calibration():
    ntp_client = ntplib.NTPClient()

    ntp_server = "ntp.tuna.tsinghua.edu.cn"
    response = ntp_client.request(ntp_server, version=4)
    ntp_time = datetime.datetime.utcfromtimestamp(response.tx_time)
    local_time = datetime.datetime.utcnow()
    time_difference = local_time - ntp_time
    print("Time difference:", time_difference.total_seconds() * 1e6)
    return time_difference.total_seconds() * 1e6


if __name__ == "__main__":
    time_calibration()
