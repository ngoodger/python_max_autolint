import pytest
import unittest.mock as mock 
import max_autolint

# Rules
# Syntax error causes all checkers to fail
@pytest.fixture
def test_files():
    files = {"file_0":max_autolint.File(syntax_error=None, good=False, checker_failures=set(),
                           checker_errors=set(), checker_no_errors=set(), 
                           modifier_failures=set(), modifier_applied=set()),  
             "file_1":max_autolint.File(syntax_error=None, good=False, checker_failures=set(),
                           checker_errors=set(), checker_no_errors=set(), 
                           modifier_failures=set(), modifier_applied=set()),  
             "file_2":max_autolint.File(syntax_error=None, good=False, checker_failures=set(),
                           checker_errors=set(), checker_no_errors=set(), 
                           modifier_failures=set(), modifier_applied=set()),  
             "file_3":max_autolint.File(syntax_error=None, good=False, checker_failures=set(),
                           checker_errors=set(), checker_no_errors=set(), 
                           modifier_failures=set(), modifier_applied=set()),  
            }
    
    files["file_0"].syntax_error_present= False
    files["file_1"].syntax_error_present= False
    files["file_2"].syntax_error_present= True
    files["file_3"].syntax_error_present= False 

    files["file_0"].checker_errors_present={"isort"}
    files["file_1"].checker_errors_present={"isort", "black"}
    files["file_2"].checker_errors_present=set()
    files["file_3"].checker_errors_present={"flake8"}
    return files

class TestAutoLint():

    @staticmethod
    def mock_modifier(files, name, check=False,):
        for _, file in files.items():
            if not file.syntax_error_present:
                if name in file.checker_errors_present:
                    if name in file.checker_errors:
                        file.checker_errors.remove(name)
                    file.checker_no_errors.add(name)
                    file.modifier_applied.add(name)
            else:
                file.modifier_failures.add(name)

    def mock_checker(files, name):
        for _, file in files.items():
            if not file.syntax_error_present:
                if name in file.checker_errors_present:
                    file.checker_errors.add(name)
                else:
                    file.checker_no_errors.add(name)
            else:
                file.checker_failures.add(name)

    @staticmethod
    def mock_black(files, check=False):
        if check:
            TestAutoLint.mock_checker(files, "black")
        else:
            TestAutoLint.mock_modifier(files, "black")

    @staticmethod
    def mock_isort(files, check=False):
        if check:
            TestAutoLint.mock_checker(files, "isort")
        else:
            TestAutoLint.mock_modifier(files, "isort")

    @staticmethod
    def mock_syntax(files):
        for _, file in files.items():
            file.syntax_error = file.syntax_error_present

    @staticmethod
    def mock_flake8(files):
        TestAutoLint.mock_checker(files, "flake8")

    def test_check(self,test_files):
        test_type= "unit"
        if test_type == "unit":

            autolinter = max_autolint.MaxAutolint()
            autolinter.modifiers=[TestAutoLint.mock_black, TestAutoLint.mock_isort]
            autolinter.checkers=[TestAutoLint.mock_flake8]
            autolinter.syntax=TestAutoLint.mock_syntax

        else:
            raise NotImplemented

        autolinter.check_syntax(test_files)
        autolinter.check(test_files)

        # Check that the corresponding errors and modifiers have been detected.
        for _, file in test_files.items():
            if file.syntax_error_present:
                assert(file.syntax_error), "File with syntax error should be detected"
                assert(file.checker_failures
                       == {"black", "isort", "flake8"}), "All checkers should fail due to syntax error."
                #assert(file.modifier_failures
                #       == autolinter.modifiers), "All modifiers should fail due to syntax error."
            else:
                assert(file.checker_errors_present
                       == file.checker_errors), "Error raised flag does not match expected."
                assert(
                   len(file.modifier_applied)==0), "No modifiers applied yet"
            if len(file.checker_errors) > 0:
                assert(not file.good), "Presence of checker errors indicates bad file."

    def test_modify(self, test_files):
        test_type= "unit"
        if test_type == "unit":

            autolinter = max_autolint.MaxAutolint()
            autolinter.modifiers=[TestAutoLint.mock_black, TestAutoLint.mock_isort]
            autolinter.checkers=[TestAutoLint.mock_flake8]
            autolinter.syntax=TestAutoLint.mock_syntax

        else:
            raise NotImplemented

        autolinter.check_syntax(test_files)
        autolinter.check(test_files)
        autolinter.modify(test_files)
        for _, file in test_files.items():
            assert(not "isort" in file.checker_errors), "Black should be resolved."
            if "black" in file.checker_errors_present:
                assert(not "black" in file.checker_errors), "Black should be resolved."
                assert("black" in file.modifier_applied), "Black should be listed in modifiers applied."
            if "isort" in file.checker_errors_present:
                assert(not "isort" in file.checker_errors), "Isort should be resolved."
                assert("isort" in file.modifier_applied), "Isort should be listed in modifiers applied."
            if file.syntax_error_present or "flake8" in file.checker_errors:
                assert(not file.good), "Checker errors should not be resolvable."
            else:
                assert(file.good), "Checker errors should be resolved."
            if file.syntax_error_present:
                assert(file.checker_failures
                       == {"black", "isort", "flake8"}), "All checkers should fail due to syntax error."
                assert(file.modifier_failures
                       == {"black", "isort"}), "All modifiers should fail due to syntax error."
