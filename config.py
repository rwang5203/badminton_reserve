# URLs for Court Reservation
ALIVE_URL = "https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook"
LOGIN_URL = "https://50.tsinghua.edu.cn/j_spring_security_check"
HOMEPAGE_URL = "http://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewIndex"
PHONE_URL = "https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=hadContactOrNot"
BOOK_URL = "https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=saveGymBook"
ORDER_URL = "https://50.tsinghua.edu.cn/pay/payAction.do?ms=getOrdersForNopay"
CAPTCHA_URL = "https://50.tsinghua.edu.cn/Kaptcha.jpg"
TOKEN_URL = "https://50.tsinghua.edu.cn/userOperation.do?ms=gotoLoginPage"

# URLs for Automated Payment (TODO: requires WeChat Pay/Alipay API)
PAY_JUDGE_URL = "https://50.tsinghua.edu.cn/pay/payAction.do?ms=judgeHavePayed"
THU_PAY_URL = "http://fa-online.tsinghua.edu.cn/zjjsfw/zjjs/api.do"


# Format Headers and URL
def format_viewbook_url(
    gym_id: str,
    item_id: str,
    book_date: str,
) -> str:
    return f"https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id={gym_id}&item_id={item_id}&time_date={book_date}&userType=1"


def format_captcha_header(
    server_id,
    jsession_id,
    gym_id: str,
    item_id: str,
    book_date: str,
) -> dict:
    captcha_header = {
        "accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": f"serverid={server_id}; JSESSIONID={jsession_id}",
        "referer": f"https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id={gym_id}&item_id={item_id}&time_date={book_date}&userType=",
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
    server_id,
    jsession_id,
    gym_id: str,
    item_id: str,
    book_date: str,
) -> dict:
    book_header = {
        "host": "50.tsinghua.edu.cn",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "content-length": "339",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"serverid={server_id}; JSESSIONID={jsession_id}",
        "origin": "https://50.tsinghua.edu.cn",
        "referer": f"https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id={gym_id}&item_id={item_id}&time_date={book_date}&userType=",
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
    costs: list,
    index: int,
    tokens: list,
    phone_num: str,
    gym_id: str,
    item_id: str,
    book_date: str,
    captcha_label: str,
    payment_method: str = "offline",
) -> dict:
    print("COSTS:", costs)
    book_data = {
        "bookData.totalCost": costs[index % len(tokens)],
        "bookData.book_person_zjh": "",
        "bookData.book_person_name": "",
        "bookData.book_person_phone": phone_num,
        "gymnasium_idForCache": gym_id,
        "item_idForCache": item_id,
        "time_dateForCache": book_date,
        "userTypeNumForCache": "1",
        "code": captcha_label,
        "putongRes": "putongRes",
        "selectedPayWay": 1 if payment_method == "online" else 0,
        "allFieldTime": tokens[index % len(tokens)] + "#" + book_date,
    }
    return book_data


def format_pay_header(server_id, jsession_id) -> dict:
    pay_header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-length": "43",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"JSESSIONID={jsession_id}; serverid={server_id}",
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
