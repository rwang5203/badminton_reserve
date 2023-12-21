'''
A global module that stored in actively read and modified by all modules.
'''
import requests
from model import CNN
from selenium.webdriver import Chrome


book_data: dict
book_date: str
book_headers: dict
captcha_headers: dict
chromeDriver: Chrome
index: int = 0
jsessionid = None
serverid = None
captcha_label: str
cuda_device: str
curCourtIDs: int
payment_method: int
password: str
phone_number: str
prefGymID: str
prefGymNameCN: str
prefGymNameEN: str
prefItemID: str
prefCourtIDs: list = []
validCourtIDs: list = []
prefCourtCosts: list = []
prefCourtInfos = []
prefCourtTokens = []
recognition_model: CNN
session: requests.Session
studentid: str
time_difference: float = None
userName: str = None
viewbookURL: str = None
