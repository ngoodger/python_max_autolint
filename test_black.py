import pytest
import max_autolint

@pytest.fixture()
def unformatted_filename(tmp_path):
    unformatted_filename = f"{tmp_path}/unformatted_code.py"
    # Missing spaces around operator +.
    with open(unformatted_filename, "w") as f:
        f.write("a = 1+2")
    return unformatted_filename 

@pytest.fixture()
def formatted_filename(tmp_path):
    formatted_filename = f"{tmp_path}/formatted_code.py"
    # Correctly formatted.
    with open(formatted_filename, "w")  as f:
        f.write("a = 1 + 2")
    return formatted_filename 

def test_black_check_unformatted(unformatted_filename):
    """
    Test python black correctly reports change required for unformatted code.
    """
    files = {unformatted_filename: max_autolint.File(path=unformatted_filename, checker_failures=set(), checker_errors=set(),

                      checker_no_errors=set(), modifier_applied=set(), modifier_failures=set())}
    black = max_autolint.Black(files, modifier=False)
    # Start black.
    black()
    while not black.done():
        # Wait until done.
        pass
    assert(files[unformatted_filename].checker_errors == {"Black"})
    assert("unformatted_code.py" in unformatted_filename)

def test_black_modify_unformatted(unformatted_filename):
    """
    Test python black correctly reformats unformatted code.
    """
    files = {unformatted_filename: max_autolint.File(path=unformatted_filename, checker_failures=set(), checker_errors=set(),

                      checker_no_errors=set(), modifier_applied=set(), modifier_failures=set())}
    black = max_autolint.Black(files, modifier=True)
    # Start black.
    black()
    while not black.done():
        # Wait until done.
        pass
    assert(files[unformatted_filename].modifier_applied == {"Black"})
    assert("unformatted_code.py" in unformatted_filename)
    
   
def test_black_check_formatted(formatted_filename):
    """
    Test python black correctly reports no change required for formatted code.
    """
    assert("formatted_code.py" in formatted_filename)
