from tap import Tap
from typing import Literal, List, Union


class Args(Tap):
    studentid: str  # 学号
    password: str
    phone: str
    paymentmethod: int = 0  # (0 for on-site payment, 1 for online payment)
    booknow: bool = False  # Book immediately, for testing.
    gym: Literal['Qimo', 'Zongti', 'Xiti', 'Tennis'] = 'Tennis'
    '''[气膜："Qimo", 综体："Zongti", 西体："Xiti"]'''
    fields: List[int] = []
    '''
    目标场地，可以用数字或者字符串表示，例如：3 -> 三号场地，比如气膜的 "羽03".
    '''
