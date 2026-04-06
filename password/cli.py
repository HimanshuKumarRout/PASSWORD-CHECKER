import argparse
import getpass
from typing import List

from .scorer import score_password


def _format_feedback(lines: List[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check password strength.")
    parser.add_argument("password", nargs="?", default=None, help="Password to check (optional, will prompt if omitted).")
    parser.add_argument(
        "--min-score",
        type=int,
        default=None,
        help="If provided, exit with code 2 when score is below this value.",
    )
    args = parser.parse_args()

    if args.password is None:
        pwd = getpass.getpass("Enter password (input hidden): ")
    else:
        pwd = args.password

    strength = score_password(pwd)

    print(f"Score: {strength.score}/100")
    print(f"Strength: {strength.label}")
    print("Feedback:")
    print(_format_feedback(strength.feedback))

    if args.min_score is not None and strength.score < args.min_score:
        return 2
    return 0

