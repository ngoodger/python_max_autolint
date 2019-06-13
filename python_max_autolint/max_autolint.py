import logging
import sys

from python_max_autolint import agent, file_set, git_collect_file_set, ops


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
    my_isort = ops.IsortChecker() if check_only else ops.IsortModifier()
    my_black = ops.BlackChecker() if check_only else ops.BlackModifier()
    ops_set = {my_syntax, my_flake8, my_black, my_isort}
    my_file_set = file_set.FileSet(files, ops_to_run=ops_set)

    my_agent = agent.OrderedAgent(file_set=my_file_set, ops=ops_set)
    logger.debug(f"Starting max autolint now..")
    result = my_agent()
    # If result is not None.  Indicative of issue. Output std_out and std_error.
    if result is not None:
        sys.stdout.write(result.std_out)
        sys.stderr.write(result.std_error)
