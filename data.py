import requests
from model import CNN


class Data:
    '''
    A global variable that stored in actively read and modified by all modules.
    '''
    book_data: dict = None
    book_date: str = None
    book_headers: dict = None
    captcha_headers: dict = None
    chromeDriver = None
    index = 0
    jsessionid = None
    serverid = None
    captcha_label: str = None
    cuda_device: str = None
    curCourtIDs = None
    payment_method: int = None
    password: str = None
    phone_number: str = None
    prefGymID: str = None
    prefGymNameCN: str = None
    prefGymNameEN: str = None
    prefItemID: str = None
    prefCourtIDs: list = []
    validCourtIDs: list = []
    prefCourtCosts: list = []
    prefCourtInfos = []
    prefCourtTokens = []
    recognition_model: CNN = None
    session: requests.Session = None
    studentid: str = None
    time_difference: float = None
    userName: str = None
    viewbookURL: str = None
