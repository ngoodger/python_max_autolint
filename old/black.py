from max_autolint import FileOperator


class BlackChecker(FileOperator):
    ERROR_INDICATOR_STRING = "error: cannot format "
    ERROR_START_FILE_IDX = len(ERROR_INDICATOR_STRING)
    WOULD_REFORMAT_INDICATOR_STRING = "would reformat "
    WOULD_REFORMAT_START_FILE_IDX = len(WOULD_REFORMAT_INDICATOR_STRING)

    def __init__(self, files: str, modifier: bool):
        super(BlackChecker, self).__init__(files)
        self.modifier = modifier
        self._base_cmd = ["black", "--check"]
        self._resolvers = {self.__type__.name}

    def get_filenames_of_interest(indicator_string: str, input_string: str):
        input_lines = input_string.splitlines()
        input_lines = (line for line in input_lines if indicator_string in line)
        filenames = (input_line[len(indicator_string) :] for input_line in input_lines)
        return filenames

    @property
    def resolvers(self):
        return self._resolvers

    @property
    def base_cmd(self):
        return self._base_cmd

    @property
    def resolvers(self):
        return self._resolvers

    def out_update_file_properties(self, outs: str):
        pass

    def err_update_file_properties(self, err: str):
        error_filenames = self.get_filenames_of_interest(
            self.ERROR_INDICATOR_STRING, err
        )
        for error_filename in error_filenames:
            self.files[error_filename].checker_failed.add(type(self).__name__)
        if self.modifier:
            reformatted_filenames = self.get_filenames_of_interest(
                self.REFORMAT_INDICATOR_STRING, err
            )
            for reformatted_filename in reformatted_filenames:
                self.files[reformatted_filename].modifier_applied.add(
                    type(self).__name__
                )
        else:
            would_reformat_filenames = self.get_filenames_of_interest(
                self.WOULD_REFORMAT_INDICATOR_STRING, err
            )
            for would_reformat_filename in would_reformat_filenames:
                self.files[would_reformat_filename].checker_errors.add(
                    type(self).__name__
                )


class BlackModifier(FileOperator):
    # Start file path comes after reformatted + space.
    REFORMAT_INDICATOR_STRING = "reformatted "
    REFORMAT_START_FILE_IDX = len(REFORMAT_INDICATOR_STRING)
    ERROR_INDICATOR_STRING = "error: cannot format "
    ERROR_START_FILE_IDX = len(ERROR_INDICATOR_STRING)

    def __init__(self, files: str, modifier: bool):
        super(BlackModifier, self).__init__(files)
        self.modifier = modifier
        self._base_cmd = ["black"]
        self._resolvers = {self.__type__.name}

    @property
    def resolvers(self):
        return self._resolvers

    @property
    def base_cmd(self):
        return self._base_cmd

    def out_update_file_properties(self, outs: str):
        pass

    def err_update_file_properties(self, err: str):
        error_filenames = self.get_filenames_of_interest(
            self.ERROR_INDICATOR_STRING, err
        )
        for error_filename in error_filenames:
            self.files[error_filename].checker_failed.add(type(self).__name__)
        if self.modifier:
            reformatted_filenames = self.get_filenames_of_interest(
                self.REFORMAT_INDICATOR_STRING, err
            )
            for reformatted_filename in reformatted_filenames:
                self.files[reformatted_filename].modifier_applied.add(
                    type(self).__name__
                )
        else:
            would_reformat_filenames = self.get_filenames_of_interest(
                self.WOULD_REFORMAT_INDICATOR_STRING, err
            )
            for would_reformat_filename in would_reformat_filenames:
                self.files[would_reformat_filename].checker_errors.add(
                    type(self).__name__
                )
