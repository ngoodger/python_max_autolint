from dataclasses import dataclass
import subprocess as sp
from abc import ABC, abstractmethod
from typing import Dict

@dataclass
class File:
    checker_failures: set
    checker_errors: set
    checker_no_errors: set
    modifier_applied: set
    modifier_failures: set
    path: str
    syntax_error: bool=None
    good: bool=False

def check_error(file):
    pass

class FileOperator(ABC):

    def __init__(self, files: Dict[str, File]):
        self.files = files
        
    def __call__(self):
        self.proc = sp.Popen(self.base_cmd + list(self.files.keys()),stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)

    def done(self):
        proc_done = not self.proc.poll() is None
        # If process is finished update file properties according to stdout and stderr.
        if proc_done: 
            out, err= self.proc.communicate(timeout=1)
            self.out_update_file_properties(out)
            self.err_update_file_properties(err)
        return proc_done

    @staticmethod
    def get_filenames_of_interest(indicator_string: str, input_string: str):
        print("get_filenames_of_interest")
        print(input_string)
        input_lines = input_string.splitlines()
        print(input_lines)
        input_lines = (line for line in input_lines if indicator_string in line)
        filenames = (input_line[len(indicator_string):] for
                                 input_line in input_lines)
        return filenames

    @property
    @abstractmethod
    def base_cmd(self):
        pass

    @abstractmethod
    def out_update_file_properties(self):
        pass

    @abstractmethod
    def err_update_file_properties(self):
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
    WOULD_REFORMAT_INDICATOR_STRING = "would reformat "
    WOULD_REFORMAT_START_FILE_IDX = len(WOULD_REFORMAT_INDICATOR_STRING) 

    def  __init__(self, files: str, modifier: bool):
        super(Black, self).__init__(files)
        self.modifier = modifier
        if self.modifier:
            self._base_cmd =["black"]
        else:
            self._base_cmd =["black", "--check"]
            

    @property
    def base_cmd(self):
        return self._base_cmd 


    def out_update_file_properties(self, outs: str):
        pass

    def err_update_file_properties(self, err: str):
        error_filenames = self.get_filenames_of_interest(self.ERROR_INDICATOR_STRING, err)
        for error_filename in error_filenames:
            self.files[error_filename].checker_failed.add(type(self).__name__)
        if self.modifier:
            reformatted_filenames = self.get_filenames_of_interest(self.REFORMAT_INDICATOR_STRING, err)
            for reformatted_filename in reformatted_filenames:
                self.files[reformatted_filename].modifier_applied.add(type(self).__name__)
        else:
            would_reformat_filenames = self.get_filenames_of_interest(self.WOULD_REFORMAT_INDICATOR_STRING, err)
            for would_reformat_filename in would_reformat_filenames:
                self.files[would_reformat_filename].checker_errors.add(type(self).__name__)
        

class Isort(Modifier):
    pass

class Flake8(Checker):
    pass

class Syntax(Checker):
    pass


class MaxAutolint(object):

    def __init__(self):
        #self._modifiers={Isort(), Black()}
        #self._checkers={Flake8}
        self._syntax=Syntax

    def check_syntax(self, files):
        self._syntax.__call__(files)

    def check_good(self, files):
        for _, file in files.items():
            syntax_error_checked = file.syntax_error is not None
            all_checkers_run_no_errors = len(self.checkers) == len(file.checker_no_errors)
            file.good = syntax_error_checked and all_checkers_run_no_errors
        
    def check(self, files):
        for checker in self._checkers:
            checker(files)
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
