import argparse
import agent
import black
import flake8
import syntax
import git_collect_file_set

def main(path: str, check_only: bool):
    file_collector = git_collect_file_set.GitCollectFileSet(path)

    my_flake8 = flake8.Flake8()
    my_black= black.Black()

    my_syntax = syntax.Syntax()
    checkers = [flake8]
    modifiers = [my_black] 

    my_agent = agent.Agent(file_collector=file_collector, syntax=my_syntax,
                           checkers=checkers, modifiers=modifiers)
    my_agent(check_only)

def dir_path(path):
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
