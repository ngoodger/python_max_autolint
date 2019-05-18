import pytest
import unittest.mock as mock
import max_autolint
from abc import ABC, abstractmethod

# Rules
# Syntax error causes all checkers to fail
@pytest.fixture
def test_files():
    files = {
        "file_0": max_autolint.File(
            path="file_0",
            syntax_error=None,
            good=False,
            checker_failures=set(),
            checker_errors=set(),
            checker_no_errors=set(),
            modifier_failures=set(),
            modifier_applied=set(),
        ),
        "file_1": max_autolint.File(
            path="file_1",
            syntax_error=None,
            good=False,
            checker_failures=set(),
            checker_errors=set(),
            checker_no_errors=set(),
            modifier_failures=set(),
            modifier_applied=set(),
        ),
        "file_2": max_autolint.File(
            path="file_2",
            syntax_error=None,
            good=False,
            checker_failures=set(),
            checker_errors=set(),
            checker_no_errors=set(),
            modifier_failures=set(),
            modifier_applied=set(),
        ),
        "file_3": max_autolint.File(
            path="file_3",
            syntax_error=None,
            good=False,
            checker_failures=set(),
            checker_errors=set(),
            checker_no_errors=set(),
            modifier_failures=set(),
            modifier_applied=set(),
        ),
    }

    files["file_0"].syntax_error_present = False
    files["file_1"].syntax_error_present = False
    files["file_2"].syntax_error_present = True
    files["file_3"].syntax_error_present = False

    # Representing real file properties as strings.
    files["file_0"].checker_errors_present = {"isort"}
    files["file_1"].checker_errors_present = {"isort", "black"}
    files["file_2"].checker_errors_present = set()
    files["file_3"].checker_errors_present = {"flake8"}
    return files


class MockModifier:
    def mock_modifier(self, files):
        for _, file in files.items():
            if not file.syntax_error_present:
                if str(self) in file.checker_errors_present:
                    if str(self) in file.checker_errors:
                        file.checker_errors.remove(str(self))
                    file.checker_no_errors.add(str(self))
                    file.modifier_applied.add(str(self))
            else:
                file.modifier_failures.add(str(self))


class MockChecker:
    def mock_checker(self, files):
        for _, file in files.items():
            if not file.syntax_error_present:
                if str(self) in file.checker_errors_present:
                    file.checker_errors.add(str(self))
                else:
                    file.checker_no_errors.add(str(self))
            else:
                file.checker_failures.add(str(self))

    @abstractmethod
    def __repr__(self):
        pass


class MockBlackChecker(MockChecker):
    def __call__(self, files):
        self.mock_checker(files)

    def __repr__(self):
        return "black"


class MockBlackModifier(MockModifier):
    def __call__(self, files):
        self.mock_modifier(files)

    def __repr__(self):
        return "black"


class MockIsortChecker(MockChecker):
    def __call__(self, files):
        self.mock_checker(files)

    def __repr__(self):
        return "isort"


class MockIsortModifier(MockModifier):
    def __call__(self, files):
        self.mock_modifier(files)

    def __repr__(self):
        return "isort"


class MockSyntax:
    def __call__(self, files):
        for _, file in files.items():
            file.syntax_error = file.syntax_error_present

    def __repr__(self):
        return "syntax"


class MockFlake8Checker(MockChecker):
    def __call__(self, files):
        self.mock_checker(files)

    def __repr__(self):
        return "flake8"


class TestAutoLint:
    @staticmethod
    def test_check(test_files):
        """
        Test check function of max_autolint.
        """
        test_type = "unit"
        if test_type == "unit":

            autolinter = max_autolint.MaxAutolint()
            autolinter.modifiers = [MockBlackModifier(), MockIsortModifier()]
            autolinter.checkers = [
                MockFlake8Checker(),
                MockBlackChecker(),
                MockIsortChecker(),
            ]
            autolinter.syntax = MockSyntax()

        else:
            raise NotImplemented

        autolinter.check_syntax(test_files)
        autolinter.check(test_files)

        # Check that the corresponding errors and modifiers have been detected.
        for _, file in test_files.items():
            if file.syntax_error_present:
                assert file.syntax_error, "File with syntax error should be detected"
                assert file.checker_failures == {
                    "black",
                    "isort",
                    "flake8",
                }, "All checkers should fail due to syntax error."
                # assert(file.modifier_failures
                #       == autolinter.modifiers), "All modifiers should fail due to syntax error."
            else:
                assert (
                    file.checker_errors_present == file.checker_errors
                ), "Error raised flag does not match expected."
                assert len(file.modifier_applied) == 0, "No modifiers applied yet"
            if len(file.checker_errors) > 0:
                assert not file.good, "Presence of checker errors indicates bad file."

    @pytest.mark.parametrize(
        "check_first", (True, False), ids=["checker_first", "do_not_check_first"]
    )
    def test_modify(self, test_files, check_first):
        """
        Test modify of max_autolint. 
        """
        test_type = "unit"
        if test_type == "unit":

            autolinter = max_autolint.MaxAutolint()
            autolinter.modifiers = {MockBlackModifier(), MockIsortModifier()}
            autolinter.checkers = {
                MockBlackChecker(),
                MockIsortChecker(),
                MockFlake8Checker(),
            }
            autolinter.syntax = MockSyntax()

        else:
            raise NotImplemented

        if check_first:
            autolinter.check_syntax(test_files)
            autolinter.check(test_files)
        autolinter.modify(test_files)
        for _, file in test_files.items():
            assert not "isort" in file.checker_errors, "Black should be resolved."
            if "black" in file.checker_errors_present:
                assert not "black" in file.checker_errors, "Black should be resolved."
                assert (
                    "black" in file.modifier_applied
                ), "Black should be listed in modifiers applied."
            if "isort" in file.checker_errors_present:
                assert not "isort" in file.checker_errors, "Isort should be resolved."
                assert (
                    "isort" in file.modifier_applied
                ), "Isort should be listed in modifiers applied."
            if file.syntax_error_present or len(file.checker_no_errors) < len(
                autolinter.checkers
            ):
                assert not file.good, "Checker errors should not be resolvable."
            else:
                assert file.good, "Checker errors should be resolved."
            if file.syntax_error_present:
                assert file.modifier_failures == {
                    "black",
                    "isort",
                }, "All modifiers should fail due to syntax error."
