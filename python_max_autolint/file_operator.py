import logging
import math
import subprocess as sp
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List

MS_IN_SECOND = 1000
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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


class FileOperator(ABC):
    def __init__(self):
        self.result = None

    def __call__(self, files: List[str]):
        self.start_time = time.time()
        self.proc = sp.Popen(
            self.base_cmd + files,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            universal_newlines=True,
        )

    def check_done(self):
        proc_done = not self.proc.poll() is None
        # If process is finished update file properties according to stdout and stderr.
        if proc_done:
            self.std_out, self.std_error = self.proc.communicate(timeout=1)
            self.return_code = self.return_code_lookup(self.proc.returncode)
            self.end_time = time.time()
            self.elapsed_time_ms = math.ceil(
                (self.end_time - self.start_time) * MS_IN_SECOND
            )
            self.result = FileOperatorReturn(
                error=not self.return_code == SubProcessReturnCode.SUCCESS,
                std_out=self.std_out,
                std_error=self.std_error,
                elapsed_time_ms=self.elapsed_time_ms,
            )
            logger.debug(f"{self.__class__} elapsed_time {self.elapsed_time_ms}ms")
        return proc_done

    @property
    @abstractmethod
    def modifying(self):
        pass

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

    @property
    @abstractmethod
    def run_first(self):
        pass

    @property
    @abstractmethod
    def reporting_priority(self):
        """
        Used for prioritising return messages. Lower is higher priority.
        """

    def return_code_lookup(self, return_code: int):
        if return_code == self.success_return_int:
            return SubProcessReturnCode.SUCCESS
        elif return_code == self.error_return_int:
            return SubProcessReturnCode.ERROR
        else:
            return SubProcessReturnCode.FAIL

    def __repr__(self):
        return str(type(self).__name__)
