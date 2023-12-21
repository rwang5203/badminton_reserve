# Badminton Reserve with Selenium

## Usage

Installed the python environment (PyTorch, Selenium, OpenCV, typed-argument-parser, NumPy):

```shell
pip install -r requirements.txt
```

Run the following command:

```shell
python main.py --studentid <学号> --phone <手机号码> --password <密码> --fields 4 5 6 7 8 9 10 --gym Qimo --paymentmethod 1
```

Run `python main.py -h` to see all arguments.

> Make sure your machine's clock is not too off. Go to <https://time.is/> to check.

## TODOs

- Code adaptation to Ubuntu and performance testing (automate.py & book_court.py)
- AliPay automatic payment (automate.py)
