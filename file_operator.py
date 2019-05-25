import time
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from typing import List
import subprocess as sp
import math


@dataclass
class FileOperatorReturn:
    error: bool
    std_out: str
    std_error: str
    elapsed_time_ms: int


class SubProcessReturnCode(Enum):
    # SUCCESS indicates successful operation i.e. check with no errors / modify no errors.
    SUCCESS = 0
    # ERROR indicates successful failure i.e. check did not pass due to unused variable.
    ERROR = 1
    # FAIL indicates check or modify did not work.  i.e. syntax error except for syntax checker.
    FAIL = 2


MS_IN_SECOND = 1000


class FileOperator(ABC):
    def __call__(self, files: List[str]):
        start_time = time.time()
        SLEEP_TIME_SEC = 0.01
        self.proc = sp.Popen(
            self.base_cmd + files,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            universal_newlines=True,
        )
        # Wait until done.
        proc_done = self.check_done()
        while not proc_done:
            time.sleep(SLEEP_TIME_SEC)
            proc_done = self.check_done()

        # Now we are done get elapsed time and build result.
        end_time = time.time()
        elapsed_time_ms = math.ceil((end_time - start_time) * MS_IN_SECOND)

        result = FileOperatorReturn(
            error=not self.return_code == SubProcessReturnCode.SUCCESS,
            std_out=self.std_out,
            std_error=self.std_error,
            elapsed_time_ms=elapsed_time_ms,
        )
        return result

    def check_done(self):
        proc_done = not self.proc.poll() is None
        # If process is finished update file properties according to stdout and stderr.
        if proc_done:
            self.std_out, self.std_error = self.proc.communicate(timeout=1)
            self.return_code = self.return_code_lookup(self.proc.returncode)
        return proc_done

    @property
    @abstractmethod
    def base_cmd(self):
        pass

    @property
    @abstractmethod
    def success_return_int(self):
        pass

    @property
    @abstractmethod
    def error_return_int(self):
        pass

    def return_code_lookup(self, return_code: int):
        if return_code == self.success_return_int:
            return SubProcessReturnCode.SUCCESS
        elif return_code == self.error_return_int:
            return SubProcessReturnCode.ERROR
        else:
            return SubProcessReturnCode.FAIL
