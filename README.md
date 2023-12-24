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

> Make sure your local system's time is calibrated. You can calibrate your local time with Tsinghua NTP server `ntp.tuna.tsinghua.edu.cn` in advance to your reserving.

### Chrome Driver Configuration
For all platforms, you can download the latest chrome driver [here](https://googlechromelabs.github.io/chrome-for-testing/).
#### Linux
After unzipping the `chromedriver-linux64.zip` to `/path/to/chromedriver-linux64`, configure the driver directory in `automate.py` through the following code.
```python
chrome_options.binary_location = '/path/to/chromedriver-linux64'
```

#### Windows
After unzipping `chromedriver-win64.zip` to `/path/to/chromedriver-win64`, configure the driver path in `automate.py` through the following code.
```python
chrome_driver_path = '/path/to/chromedriver-win64.exe'

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
```


## TODOs

- Code adaptation to macOS and performance testing (automate.py, book_court.py)
- Concurrent multiuser booking (main.py, book_court.py, globals.py)
- AliPay automatic payment (automate.py)
