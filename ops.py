import file_operator


class Syntax(file_operator.FileOperator):

    @property
    def base_cmd(self):
        return ["python3", "-m", "py_compile"]
    @property
    def success_return_int(self):
        return 0
    @property
    def error_return_int(self):
        return 1
    @property
    def locking(self):
        return False 
    @property
    def reporting_priority(self):
        return 0

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
    @property
    def locking(self):
        return True 
    @property
    def reporting_priority(self):
        return 1



class BlackChecker(file_operator.FileOperator):

    @property
    def base_cmd(self):
        return ["black", "--check"]
    @property
    def success_return_int(self):
        return 0
    @property
    def error_return_int(self):
        return 1

    @property
    def locking(self):
        return False
    @property
    def reporting_priority(self):
        return 1

class Flake8(file_operator.FileOperator):

    @property
    def base_cmd(self):
        return [
            "flake8",
            "--ignore=E203,E266,E501,W503",
            "--max-complexity=18",
            "--max-line-length=80",
            "--select=B,C,E,F,W,T4,B9",
        ]
    @property
    def success_return_int(self):
        return 0

    @property
    def error_return_int(self):
        return 1

    @property
    def locking(self):
        return False 
    @property
    def reporting_priority(self):
        return 2
