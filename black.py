import file_operator


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
