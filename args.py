import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Script to book badminton courts")

    parser.add_argument("--studentid", nargs="+", type=str, required=True, help="List of Student IDs")
    parser.add_argument("--password", nargs="+", type=str, required=True, help="List of Passwords")
    parser.add_argument("--phone", nargs="+", type=str, required=True, help="List of Phone numbers")
    parser.add_argument("--paymentmethod", type=int, default=0, choices=[0, 1], help="Payment method: 0 for on-site, 1 for online")
    parser.add_argument("--booknow", action="store_true", help="If set, book immediately (for testing)")
    parser.add_argument("--multiuser", type=int, default=1, help="Number of users to book for")
    parser.add_argument("--gym", type=str, default="Qimo", choices=["Qimo", "Zongti", "Xiti", "Tennis"], help="Target gym")
    parser.add_argument("--fields", nargs="+", type=int, default=[12, 11, 10, 9, 8, 7], help="Target fields as a list of integers")

    args = parser.parse_args()

    if args.multiuser != len(args.studentid) or args.multiuser != len(args.password) or args.multiuser != len(args.phone):
        raise ValueError("The number of student IDs, passwords, and phone numbers should match the number specified in --multiuser")

    return args


if __name__ == "__main__":
    args = parse_args()
    print(vars(args))
