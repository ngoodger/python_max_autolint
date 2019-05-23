import file_operator
from enum import Enum

class Syntax(file_operator.FileOperator):
    @property
    def base_cmd(self):
        return ["python3","-m","py_compile"]

    @property
    def success_return_int(self):
        return 0

    @property
    def error_return_int(self):
        return 1
