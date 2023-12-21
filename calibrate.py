import ntplib
import datetime

NTP_SERVER = "ntp.tuna.tsinghua.edu.cn"

def time_calibration():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(NTP_SERVER, version=4)
    ntp_time = datetime.datetime.utcfromtimestamp(response.tx_time)
    local_time = datetime.datetime.utcnow()
    time_difference = local_time - ntp_time
    print("Time difference (ms):", time_difference.total_seconds() * 1e6)
    return time_difference.total_seconds() * 1e6


if __name__ == "__main__":
    time_calibration()
