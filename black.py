import FileOperator

class ModifierReturnCodes(Enum):
    SUCCESS = 0

class CheckerReturnCodes(Enum):
    SUCCESS = 0
    ERROR = 1

class BlackModifier(FileOperator)
    def base_cmd(self):
        return ["black"]

    @property
    def return_code(self):
        return ModifierReturnCodes
        

class BlackCheck(FileOperator)
    def base_cmd(self):
        return ["black", "--check"]

    @property
    def return_code(self):
        return CheckerReturnCodes

