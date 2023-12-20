from schedule_events import book_main
from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    p = ArgumentParser()
    p.add_argument("--studentid", required=True, help="学号")
    p.add_argument("--password", required=True)
    p.add_argument("--phonenumber", required=True)
    p.add_argument(
        "--paymentmethod",
        help="(0 for on-stire payment, 1 for online payment)",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    book_main(args)
