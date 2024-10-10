'''
A global module with global variables actively read and modified by all modules.
'''
import requests
from model.cnn import CNN
from selenium.webdriver import Chrome
from typing import Union


book_data: dict
target_date: str
book_headers: dict
captcha_headers: dict
chrome_driver: Chrome
index: int = 0
jsessionid: Union[str, None] = None
serverid: Union[str, None] = None
captcha_label: str
infer_device: str
curCourtIDs: int
payment_method: str = 'offline'
password: str
phone: str
target_gym_id: str
target_gym_name_zh: str
target_gym_name: str = 'Qimo'
target_gym_item_id: str
target_court_ids: list = []
target_court_costs: list = []
target_court_infos = []
target_court_tokens = []
captcha_recognizer: CNN
session: requests.Session
studentid: str
time_difference: Union[float, None] = None
username: str
view_book_url: str
