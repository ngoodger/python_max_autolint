from file_operator import FileOperator, SubProcessReturnCode

class Syntax(FileOperator)

    @property
    def base_cmd(self):
        return ["flake8","--ignore=E203,E266,E501,W503", "--max-complexity=18",
                "--max-line-length=80", "--select=B,C,E,F,W,T4,B9"]
    @property
    def success_return_int(self):
        return 0

    @property
    def error_return_int(self):
        return 1
