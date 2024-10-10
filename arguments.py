import argparse
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Args:
    studentid: Union[List[str], str, None] = None
    password: Union[List[str], str, None] = None
    phone: Union[List[str], str, None] = None
    paymentmethod: Optional[str] = None
    booknow: Optional[int] = None
    gym: Optional[str] = None
    fields: Optional[List[int]] = None
    days_from_now: Optional[int] = None
    accept_free_courts: Optional[int] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Script to book badminton courts")

    parser.add_argument("--studentid", nargs="+", type=str, help="List of Student IDs")
    parser.add_argument("--password", nargs="+", type=str, help="List of Passwords")
    parser.add_argument("--phone", nargs="+", type=str, help="List of Phone numbers")
    parser.add_argument("--paymentmethod", type=str, choices=['offline', 'online'], help="Payment method: 0 for on-site, 1 for online")
    parser.add_argument("--booknow", type=int, choices=[0, 1], help="If set, book immediately (for testing)")
    parser.add_argument("--gym", type=str, choices=["Qimo", "Zongti", "Xiti", "Tennis"], help="Target gym")
    parser.add_argument("--fields", nargs="+", type=int, help="Target fields as a list of integers")
    parser.add_argument("--days_from_now", type=int, help="Number of days from now to book for.")
    parser.add_argument("--accept_free_courts", type=int, choices=[0, 1], help="是否接受预约免费的场地。")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    print(vars(args))
