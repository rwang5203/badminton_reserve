from tap import Tap
from typing import Literal, List


class Args(Tap):
    studentid: str  # 学号
    password: str  # 密码
    phone: str  # 手机号码
    paymentmethod: int = 0  # (0 for on-site payment, 1 for online payment)
    booknow: bool = False  # Book immediately, for testing.

    gym: Literal['Qimo', 'Zongti', 'Xiti', 'Tennis'] = 'Qimo'
    '''[气膜："Qimo", 综体："Zongti", 西体："Xiti"]'''

    fields: List[int] = [12, 11, 10]
    '''
    目标场地，用 int 来表示，例如：3 -> 三号场地，比如气膜的 "羽03".
    '''

    headless: bool = False  # If True, run Chrome in headless mode.
