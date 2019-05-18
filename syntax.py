import FileOperator

class CheckerReturnCodes(Enum):
    SUCCESS = 0
    ERROR = 1

class Syntax(FileOperator)
    def base_cmd(self):
        return ["python3","-m","pycompile"]

    @property
    def return_code(self):
        return CheckerReturnCodes
