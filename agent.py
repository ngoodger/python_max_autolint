import logging
from dataclasses import dataclass
import time
import file_set

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class FileSet:
    files: list 
    syntax_run: set
    checkers_run: set
    modifiers_run: set
    good: bool
    lock: bool


class Agent:
    """
    Orchestrates file set modification / checking.
    """

    def __init__(self, ops, file_set):
        self.file_set = file_set
        self.ops = ops

    def __call__(self):

        # Collect files for checking and modification.
        logger.debug(f"Files to check: {self.file_set}")

        # Only run tools if there is actually something to run them on.
        if len(self.file_set) == 0:
            logger.info("No files to check.")
            return 
        while not self.file_set.finished:
            self.file_set.update(self.ops)
            time.sleep(0.01)

        file_set.report(self.ops)
            
        """
        # Call check syntax.
        ops.syntax(files)
        # Wait until check syntax is finished.
        syntax_return = self.syntax.wait_done()
        if syntax_return.error:
            return syntax_return
        logger.debug(
            f"{self.syntax.__class__} elapsed_time {syntax_return.elapsed_time_ms}ms"
        )

        # Apply modifiers.
        for modifier in self.modifiers:
            # Call modifier.
            modifier(files)
            # Wait until modifier is done.
            modifier_return = modifier.wait_done()
            if modifier_return.error:
                return modifier_return
            logger.debug(
                f"{modifier.__class__} elapsed_time {modifier_return.elapsed_time_ms}ms"
            )

        # Check checkers.
        for checker in self.checkers:
            # Call checker.
            checker(files)
            # Wait until checker is done.
            checker_return = checker.wait_done()
            if checker_return.error:
                return checker_return
            logger.debug(
                f"{checker.__class__} elapsed_time {checker_return.elapsed_time_ms}ms"
            )
        """
