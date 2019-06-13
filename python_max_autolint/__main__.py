import argparse
import os

from python_max_autolint import max_autolint


def dir_path(path: str):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "path", type=dir_path, help="Root directory to perform modification / checking."
    )
    parser.add_argument(
        "--check_only",
        action="store_true",
        help="Only check if changes would be applied not actually apply them.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Print debug log to stdout"
    )
    args = parser.parse_args()
    max_autolint.main(args.path, args.check_only, args.debug)
