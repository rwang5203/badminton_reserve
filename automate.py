from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import datetime
import time


def automateLogin(STUDENT_ID: str, PASSWORD: str, GYM_ID: str, ITEM_ID: str, headless: bool):
    # chrome_driver_path = "./chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    if headless:
        chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--ignore-ssl-errors=yes")
    # chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("log-level=2")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )

    driver = webdriver.Chrome(options=chrome_options)
    # service = Service(chrome_driver_path)
    # driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://50.tsinghua.edu.cn/dl.jsp")

    username_field = driver.find_element(By.NAME, "un")
    password_field = driver.find_element(By.NAME, "pw")

    username_field.send_keys(STUDENT_ID)
    password_field.send_keys(PASSWORD)

    login_button = driver.find_element(
        By.XPATH, "//input[@src='images/login.jpg']"
    )
    login_button.click()

    courtBookLink = driver.find_element(
        By.XPATH,
        "//a[@href='/gymsite/gymBookViewAction.do?ms=viewBook_site&fromPage=index']",
    )
    courtBookLink.click()

    bookCourtLink = driver.find_element(
        By.XPATH, "//a[@href='javascript:viewBook()']"
    )
    bookCourtLink.click()

    confirmButton = driver.find_element(
        By.XPATH, '//button[contains(@onclick,"saveAttentionState()")]'
    )
    driver.execute_script("arguments[0].click();", confirmButton)

    gymButton = driver.find_element(
        By.XPATH,
        f"//a[@href='/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id={GYM_ID}&item_id=&time_date=&userType=']",
    )
    gymButton.click()

    curDate = str(datetime.date.today())
    curGymBadmintonButton = driver.find_element(
        By.XPATH,
        f"//a[@href='/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id={GYM_ID}&item_id={ITEM_ID}&time_date={curDate}&userType=']",
    )
    curGymBadmintonButton.click()

    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie["name"] == "serverid":
            serverid = cookie["value"]
        elif cookie["name"] == "JSESSIONID":
            jsessionid = cookie["value"]

    username = driver.find_element(
        By.XPATH, "//div[@class='member-box round-all']//strong"
    ).text

    return serverid, jsessionid, username, driver


def automatePay(driver, session, serverid, jsessionid, paymentmethod):
    orderButton = driver.find_element(
        By.XPATH, "//a[@href='/pay/payAction.do?ms=getOrdersForNopay']"
    )
    orderButton.click()

    if paymentmethod == 1:
        payNowButton = driver.find_element(
            By.XPATH, '//a[contains(@onclick, "payNow")]'
        )
        driver.execute_script("arguments[0].click();", payNowButton)

        noReceiptOption = driver.find_element(By.XPATH, '//input[@id="xm4"]')
        driver.execute_script("arguments[0].click();", noReceiptOption)

        submitButton = driver.find_element(
            By.XPATH, '//a[contains(@onclick,"savePayFrmWithPay()")]'
        )
        driver.execute_script("arguments[0].click();", submitButton)

        proceedButton = driver.find_element(
            By.XPATH, '//button[@id="proceed-button"]'
        )
        proceedButton.click()
        time.sleep(2)
        proceedButton.click()

        alipayButton = driver.find_element(
            By.XPATH, "//img[@src='/zjjsfw/img/zfb.png']"
        )
        alipayButton.click()

        # TODO: AliPay Automatic Payment
        # driver.get("http://fa-online.tsinghua.edu.cn/zjjsfw/zjjs/api.do")
        # loginAlipayButton = &lt;&nbsp;登录账户付款
