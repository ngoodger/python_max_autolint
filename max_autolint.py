import argparse
import agent
import black
import flake8
import syntax
import git_collect_file_set
import logging
import sys

logging.getLogger(__name__)

def main(path: str, check_only: bool):
    file_collector = git_collect_file_set.GitCollectFileSet(path)

    my_flake8 = flake8.Flake8()
    my_black= black.BlackChecker if check_only else black.BlackModifier()

    my_syntax = syntax.Syntax()
    checkers = [flake8]
    modifiers = [my_black]

    my_agent = agent.Agent(file_collector=file_collector, syntax=my_syntax,
                           checkers=checkers, modifiers=modifiers)
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
    parser.add_argument('-path', type=dir_path, help="Root directory to perform modification / checking.")
    parser.add_argument(
        "--check_only",
        action="store_true",
        help="Only check if changes would be applied not actually apply them.",
    )
    args = parser.parse_args()
    main(args.path, args.check_only)
