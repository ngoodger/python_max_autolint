import argparse
import agent
import ops
import git_collect_file_set
import logging
import sys
import os
import file_set


def main(path: str, check_only: bool, debug: bool):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    # file_collector = git_collect_file_set.GitCollectFileSet(path)
    file_collector = git_collect_file_set.GitCollectTrackedFileSet(path)
    # Collect files for checking and modification.
    files = file_collector()
    logger.debug(f"Files to check: {files}")

    my_syntax = ops.Syntax()
    my_flake8 = ops.Flake8()
    my_black = ops.BlackChecker() if check_only else ops.BlackModifier()
    ops_set = {my_syntax, my_flake8, my_black}
    my_file_set = file_set.FileSet(files, ops_to_run=ops_set)

    my_agent = agent.Agent(file_set=my_file_set, ops=ops_set)
    logger.debug(f"Starting max autolint now..")
    result = my_agent()
    # If result is not None.  Indicative of issue. Output std_out and std_error.
    if result is not None:
        sys.stdout.write(result.std_out)
        sys.stderr.write(result.std_error)


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
    main(args.path, args.check_only, args.debug)
