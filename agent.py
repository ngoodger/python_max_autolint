from dataclasses import dataclass
import time
import math

@dataclass
class ReturnCode:
    error :str
    elapsed_time_ms : int

class Agent():
    def __init__(self, file_collector, syntax, modifiers, checkers):

        self.file_collector = self.timeit(file_collector)
        self.syntax=self.timeit(syntax)
        self.modifiers= [self.timeit(modifier) for modifier in modifiers]
        self.checkers=[self.timeit(checker) for checker in checkers]

    @staticmethod
    def timeit(method):
        def timed(*args, **kw):
            start_time = time.time()
            error = method(*args, **kw)
            end_time = time.time()
            elapsed_time_ms = math.ceil((end_time - start_time) * 1000)
            return ReturnCode(error=error, elapsed_time_ms=elapsed_time_ms)
        return timed

    def __call__(self):

        # Collect files for checking and modification.
        files = self.file_collector()

        # Check syntax.
        syntax_return = self.syntax(files)
        if syntax_return.error is not None:
            return syntax_return.error
        print(f"check syntax elapsed_time {syntax_return.elapsed_time_ms}ms")

        # Apply modifiers. 
        for modifier in self.modifiers:
            modifier_return = modifier(files)
            if modifier_return.error is not None:
                return modifier_return.error 
            print(f"modifier elapsed_time {modifier_return.elapsed_time_ms}ms")

        # Check checkers. 
        for checker in self.checkers:
            checker_return = checker(files)
            if checker_return.error is not None:
                return checker_return.error 
            print(f"checker elapsed_time {checker_return.elapsed_time_ms}ms")
