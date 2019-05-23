from dataclasses import dataclass
import time
import math
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger

class Agent:
    """
    Orchestrates file set modification / checking.
    """
    def __init__(self, file_collector, syntax, modifiers, checkers):
        self.file_collector = file_collector
        self.syntax = syntax
        self.modifiers = modifiers
        self.checkers = checkers 

    def __call__(self):

        # Collect files for checking and modification.
        files = self.file_collector()
        logger.debug(f"Files to check: {files}")

        # Only run tools if there is actually something to run them on.
        if len(files) == 0:
            return

        # Check syntax.
        syntax_return = self.syntax(files)
        if syntax_return.error:
            return syntax_return
        logger.debug(f"{self.syntax.__class__} elapsed_time {syntax_return.elapsed_time_ms}ms")

        # Apply modifiers.
        for modifier in self.modifiers:
            modifier_return = modifier(files)
            if modifier_return.error:
                return modifier_return
            logger.debug(f"{modifier.__class__} elapsed_time {modifier_return.elapsed_time_ms}ms")

        # Check checkers.
        for checker in self.checkers:
            checker_return = checker(files)
            if checker_return.error:
                return checker_return
            logger.debug(f"{checker.__class__} elapsed_time {checker_return.elapsed_time_ms}ms")
