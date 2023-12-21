# URLs for Court Reservation
alive_url = (
    "https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook"
)
login_url = "https://50.tsinghua.edu.cn/j_spring_security_check"
homepage_url = "http://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewIndex"
phone_url = (
    "https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=hadContactOrNot"
)
book_url = "https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=saveGymBook"
order_url = "https://50.tsinghua.edu.cn/pay/payAction.do?ms=getOrdersForNopay"
captcha_url = "https://50.tsinghua.edu.cn/Kaptcha.jpg"
token_url = "https://50.tsinghua.edu.cn/userOperation.do?ms=gotoLoginPage"

# URLs for Automated Payment (TODO: May require WeChat Pay/AliPay API)
pay_judge_url = "https://50.tsinghua.edu.cn/pay/payAction.do?ms=judgeHavePayed"
thu_pay_url = "http://fa-online.tsinghua.edu.cn/zjjsfw/zjjs/api.do"


# Format Headers and URL
def format_viewbook_url(GYM_ID, ITEM_ID, BOOK_DATE) -> str:
    return f"https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id={GYM_ID}&item_id={ITEM_ID}&time_date={BOOK_DATE}&userType=1"


def format_captcha_header(
    SERVER_ID, JSESSION_ID, GYM_ID, ITEM_ID, BOOK_DATE
) -> dict:
    captcha_header = {
        "accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": f"serverid={SERVER_ID}; JSESSIONID={JSESSION_ID}",
        "referer": f"https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id={GYM_ID}&item_id={ITEM_ID}&time_date={BOOK_DATE}&userType=",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "np-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    return captcha_header


def format_book_header(
    SERVER_ID, JSESSION_ID, GYM_ID, ITEM_ID, BOOK_DATE
) -> dict:
    book_header = {
        "host": "50.tsinghua.edu.cn",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "content-length": "339",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"serverid={SERVER_ID}; JSESSIONID={JSESSION_ID}",
        "origin": "https://50.tsinghua.edu.cn",
        "referer": f"https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id={GYM_ID}&item_id={ITEM_ID}&time_date={BOOK_DATE}&userType=",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "x-requested-with": "XMLHttpRequest",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    return book_header


def format_book_data(
    COSTS: list,
    INDEX: int,
    TOKENS: list,
    PHONE_NUMBER: str,
    GYM_ID: str,
    ITEM_ID: str,
    BOOK_DATE: str,
    CAPTCHA_LABEL: str,
    PAYMENT_METHOD: int,
) -> dict:
    book_data = {
        "bookData.totalCost": COSTS[INDEX % len(TOKENS)],
        "bookData.book_person_zjh": "",
        "bookData.book_person_name": "",
        "bookData.book_person_phone": PHONE_NUMBER,
        "gymnasium_idForCache": GYM_ID,
        "item_idForCache": ITEM_ID,
        "time_dateForCache": BOOK_DATE,
        "userTypeNumForCache": "1",
        "code": CAPTCHA_LABEL,
        "putongRes": "putongRes",
        "selectedPayWay": PAYMENT_METHOD,
        "allFieldTime": TOKENS[INDEX % len(TOKENS)] + "#" + BOOK_DATE,
    }
    return book_data


def format_pay_header(SERVER_ID, JSESSION_ID) -> dict:
    pay_header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",  # noqa
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-length": "43",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"JSESSIONID={JSESSION_ID}; serverid={SERVER_ID}",
        "origin": "https://50.tsinghua.edu.cn",
        "referer": "https://50.tsinghua.edu.cn/pay/payAction.do?ms=getOrdersForNopay",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    return pay_header
