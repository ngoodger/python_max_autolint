from max_autolint import FileOperator
def test_file_operator_get_filenames_of_interest():
    indicator_string = "start of string "
    input_string = "start of string /test_file.py"
    filenames = FileOperator.get_filenames_of_interest(indicator_string, input_string)
    assert(next(filenames) == "/test_file.py")
