from dataclasses import dataclass
import subprocess as sp
from abc import ABC, abstractmethod
from typing import Dict

@dataclass
class File:
    syntax_error: bool
    good: bool
    checker_failures: set
    checker_errors: set
    checker_no_errors: set
    modifier_applied: set
    modifier_failures: set

def check_error(file):
    pass

class FileOperator(ABC):

    def __init__(self, files: Dict[str, File]):
        self.files = files
        
    def __call__(self):
        file_cmd = self.get_file_cmd(self.files)
        self.proc = sp.Popen(self.base_cmd + self.files.keys())

    def done(self):
        proc_done = not self.proc.poll() is None
        # If process is finished update file properties according to stdout and stderr.
        if proc_done: 
            proc.communicate()
            outs, errs = proc.communicate(timeout=15)
            self.update_file_properties(outs, errs)
        return proc_done

    @property
    @abstractmethod
    def base_cmd(self):
        pass

    @abstractmethod
    def update_file_properties(self):
        pass

class Modifier(ABC):
    pass

class Checker(ABC):
    pass

class PyAnnotate(Modifier):
    pass

class Mypy(Checker):
    pass

class Black(FileOperator):
    # Start file path comes after reformatted + space.
    REFORMAT_INDICATOR_STRING = "reformatted "
    REFORMAT_START_FILE_IDX = len(REFORMAT_INDICATOR_STRING) 
    ERROR_INDICATOR_STRING = "error: cannot format "
    ERROR_START_FILE_IDX = len(ERROR_INDICATOR_STRING) 

    def  __init__(self):
        self._base_cmd =["black", "--check"]

    @property
    def base_cmd():
        return self._base_cmd 

    def get_filenames_of_interest(indicator_string: str, input: str):
        input_lines = input.splitlines()
        input_lines = (line for line in input_lines if indicator_string in line)
        filenames = (input_line[indicator_string:] for
                                 input_line in input_lines)
        return filenames

    def out_update_file_properties(outs: str):
        reformatted_filenames = self.get_filenames_of_interest(self.REFORMAT_INDICATOR_STRING, outs)
        for reformatted_filename in reformatted_filenamess:
            self.files[reformatted_filename].checkers_errors = type(self).__name__

    def err_update_file_properties(err: str):
        error_filenames = self.get_filenames_of_interest(self.ERROR_INDICATOR_STRING, err)
        for error_filename in error_filenames:
            self.files[error_filename].checker_failed= type(self).__name__
        

class Isort(Modifier):
    pass

class Flake8(Checker):
    pass

class Syntax(Checker):
    pass


class MaxAutolint(object):

    def __init__(self):
        #self._modifiers=[Isort(), Black()]
        #self._checkers=[Flake8]
        self._syntax=Syntax

    def check_syntax(self, files):
        self._syntax.__call__(files)

    def check_good(self, files):
        for _, file in files.items():
            file.good = not file.syntax_error and len(file.checker_errors) == 0
        
    def check(self, files):
        for checker in self._checkers:
            checker(files)
        for modifier in self._modifiers:
            modifier(files, check=True)
        self.check_good(files)

    def modify(self, files):
        for modifier in self._modifiers:
                modifier(files)
        self.check_good(files)

    @property
    def modifiers(self):
       return self._modifiers 

    @modifiers.setter
    def modifiers(self, new_modifiers):
        self._modifiers = new_modifiers

    @property
    def checkers(self):
       return self._checkers

    @checkers.setter
    def checkers(self, new_checkers):
        self._checkers = new_checkers

    @property
    def syntax(self):
       return self._syntax

    @syntax.setter
    def syntax(self, new_syntax):
        self._syntax = new_syntax