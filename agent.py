from dataclasses import dataclass
import time
import math

class Agent:
    """
    Orchestrates file set modification / checking.
    """
    def __init__(self, file_collector, syntax, modifiers, checkers):
        self.file_collector = file_collector
        self.syntax = syntax
        self.modifiers = modifier 
        self.checkers = checkers 

    def __call__(self, check_only: bool):

        # Collect files for checking and modification.
        files = self.file_collector()

        # Check syntax.
        syntax_return = self.syntax(files)
        if syntax_return.error:
            return syntax_return
        print(f"check syntax elapsed_time {syntax_return.elapsed_time_ms}ms")

        # Apply modifiers.
        for modifier in self.modifiers:
            modifier_return = modifier(files, check_only)
            if modifier_return.error:
                return modifier_return
            print(f"modifier elapsed_time {modifier_return.elapsed_time_ms}ms")

        # Check checkers.
        for checker in self.checkers:
            checker_return = checker(files)
            if checker_return.error:
                return checker_return
            print(f"checker elapsed_time {checker_return.elapsed_time_ms}ms")
