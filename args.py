import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Script to book badminton courts")
    parser.add_argument('--studentid', type=str, required=True, help='Student ID')
    parser.add_argument('--password', type=str, required=True, help='Password')
    parser.add_argument('--phone', type=str, required=True, help='Phone number')
    parser.add_argument('--paymentmethod', type=int, default=0, choices=[0, 1], help='Payment method: 0 for on-site, 1 for online')
    parser.add_argument('--booknow', action='store_true', help='If set, book immediately (for testing)')
    parser.add_argument('--gym', type=str, default='Qimo', choices=['Qimo', 'Zongti', 'Xiti', 'Tennis'], help='Gym location')
    parser.add_argument('--fields', nargs='+', type=int, default=[12, 11, 10, 9, 8, 7], help='Target fields as a list of integers')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
