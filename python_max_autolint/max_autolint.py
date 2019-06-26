import logging
import sys

from python_max_autolint import (
    agent,
    file_set,
    git_collect_file_set,
    monitor,
    ops_set,
    runner,
)


def main(path: str, check_only: bool, debug: bool):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    # file_collector = git_collect_file_set.GitCollectFileSet(path)
    file_collector = git_collect_file_set.GitCollectTrackedFileSet(path)
    # Collect files for checking and modification.
    files = file_collector()
    logger.debug(f"Files to check: {files}")

    my_ops_set = ops_set.OpsSet()

    my_monitor = monitor.Monitor(ops_set=my_ops_set)
    my_file_set = file_set.FileSet(files=files, ops_set=my_ops_set)
    my_agent = agent.ModifiersFirstAgent(ops_set=my_ops_set)
    my_runner = runner.Runner(file_set=my_file_set, agent=my_agent, monitor=my_monitor)

    result = my_runner()

    logger.debug(f"Starting max autolint now..")
    # If result is not None.  Indicative of issue. Output std_out and std_error.
    if result is not None:
        sys.stdout.write(result.std_out)
        sys.stderr.write(result.std_error)
