# Badminton Reserve with Selenium

## Usage

Installed the python environment (PyTorch, Selenium, OpenCV, typed-argument-parser, NumPy):

```shell
pip install -r requirements.txt
```

For example, if you would like to reserve for Qimo of courts 4-10 with online payment method, you can run the following command:

```shell
python main.py --studentid <Your Student ID> --phone <Your Phone Number> --password <Your Password> --fields 4 5 6 7 8 9 10 --gym Qimo --paymentmethod 1
```

Run `python main.py -h` to see all arguments. You can also see `run_example.bat` for an example.

> Make sure your local system's time is calibrated. You can calibrate the local time with Tsinghua NTP server `ntp.tuna.tsinghua.edu.cn` in advance to your booking.

## TODOs

- Code adaptation to Ubuntu and performance testing (automate.py & book_court.py)
- AliPay automatic payment (automate.py)
