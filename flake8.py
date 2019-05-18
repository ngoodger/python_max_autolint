import FileOperator

class CheckerReturnCodes(Enum):
    SUCCESS = 0
    ERROR = 1

class Syntax(FileOperator)
    def base_cmd(self):
        return ["flake8","--ignore=E203,E266,E501,W503"]

    @property
    def return_code(self):
        return CheckerReturnCodes
