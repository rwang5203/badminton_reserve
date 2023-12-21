# Badminton Reserve with Selenium

## Usage

Installed the python environment (PyTorch, Selenium, OpenCV, typed-argument-parser, NumPy):

```shell
pip install -r requirements.txt
```

Run the following command:

```shell
python main.py --studentid <Your Student ID> --phone <Your Phone Number> --password <Your Password> --fields 4 5 6 7 8 9 10 --gym Qimo --paymentmethod 1
```

Run `python main.py -h` to see all arguments.

> Make sure your local system's clock is calibrated. You can calibrate local time with TUNA NTP server `ntp.tuna.tsinghua.edu.cn` in advance to your booking.

## TODOs

- Code adaptation to Ubuntu and performance testing (automate.py & book_court.py)
- AliPay automatic payment (automate.py)
