import file_operator
from enum import Enum

class BlackModifier(file_operator.FileOperator):
    @property
    def base_cmd(self):
        return ["black"]

    @property
    def success_return_int(self):
        return 0

    @property
    def error_return_int(self):
        return 1
        

class BlackCheck(file_operator.FileOperator):
    @property
    def base_cmd(self):
        return ["black", "--check"]

    @property
    def success_return_int(self):
        return 0

    @property
    def error_return_int(self):
        return 1
