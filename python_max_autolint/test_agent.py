from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from python_max_autolint import agent
from python_max_autolint.file_operator import FileOperatorReturn


@dataclass
class CallsTruth:
    count: int
    order: list
    arg: str


class AgentMock(agent.OrderedAgent):
    # Override init function to replace components with mocks
    def __init__(self):
        self.file_collector = Mock(return_value="test_file.py")
        return_code = FileOperatorReturn(
            error=False, std_out="std_out", std_error="std_error", elapsed_time_ms=100
        )
        self.parent_mock = Mock(return_value=return_code)
        self.parent_mock.syntax = Mock(return_value=return_code)
        self.parent_mock.modifier_0 = Mock(return_value=return_code)
        self.parent_mock.modifier_1 = Mock(return_value=return_code)
        self.parent_mock.checker_0 = Mock(return_value=return_code)
        self.parent_mock.checker_1 = Mock(return_value=return_code)
        self.syntax = self.parent_mock.syntax
        self.modifiers = [self.parent_mock.modifier_0, self.parent_mock.modifier_1]
        self.checkers = [self.parent_mock.checker_0, self.parent_mock.checker_1]


class AgentMockSyntaxFail(AgentMock):
    def __init__(self):
        super(AgentMockSyntaxFail, self).__init__()
        self.parent_mock.syntax.return_value = FileOperatorReturn(
            error=True,
            elapsed_time_ms=10,
            std_out="std_out_error_syntax",
            std_error="std_error_error_syntax",
        )


class AgentMockModifierFail(AgentMock):
    def __init__(self):
        super(AgentMockModifierFail, self).__init__()
        self.parent_mock.modifier_0.return_value = FileOperatorReturn(
            error=True,
            elapsed_time_ms=10,
            std_out="std_out_error_modifier_0",
            std_error="std_error_error_modifier_0",
        )


class AgentMockCheckerFail(AgentMock):
    def __init__(self):
        super(AgentMockCheckerFail, self).__init__()
        self.parent_mock.checker_0.return_value = FileOperatorReturn(
            error=True,
            elapsed_time_ms=10,
            std_out="std_out_error_checker_0",
            std_error="std_error_error_checker_0",
        )


def check_sideeffects(test_agent, expected):
    assert (
        len(test_agent.parent_mock.mock_calls) == expected.count
    ), "All checks should be done"
    # Check call order is correct and calls occur with correct args.
    for i, call in enumerate(expected.order):
        call == test_agent.parent_mock.mock_calls[i][0]
        expected.arg == test_agent.parent_mock.mock_calls[i][1]


"""
def test_timeit():
    SLEEP_MS = 2
    MS_IN_SECOND = 1000
    ERROR_VALUE = "test return value"

    def test_function():
        time.sleep(SLEEP_MS / MS_IN_SECOND)
        return ERROR_VALUE

    timed_test_function = agent.Agent.timeit(test_function)
    return_test = timed_test_function()

    assert (
        return_test.error == ERROR_VALUE
    ), "Error value should be passed through correctly from timed function."
    # Test time in milliseconds should always be 1 over SLEEP_MS because of function overhead
    # and ceiling function is used to round up.
    assert math.isclose(
        return_test.elapsed_time_ms, SLEEP_MS + 1
    ), "Execution time measured does not match expected in test."
"""


@pytest.mark.skip(reason="Need to update this test to suit new agent.")
def test_agent_syntax_fail():
    """
    Test agent on file containing syntax error.
    """
    test_agent = AgentMockSyntaxFail()
    TEST_OUT_SYNTAX_FAIL = CallsTruth(count=1, order=["syntax"], arg="test_file.py")
    result = test_agent()
    assert result.error
    assert result.std_out == "std_out_error_syntax"
    assert result.std_error == "std_error_error_syntax"
    check_sideeffects(test_agent, TEST_OUT_SYNTAX_FAIL)


@pytest.mark.skip(reason="Need to update this test to suit new agent.")
def test_agent_modifier_fail():
    """
    Test agent on file containing modifier_0 error.
    """
    test_agent = AgentMockModifierFail()
    TEST_OUT_MODIFIER_FAIL = CallsTruth(
        count=2, order=["syntax", "modifier_0"], arg="test_file.py"
    )
    result = test_agent()
    assert result.error
    assert result.std_out == "std_out_error_modifier_0"
    assert result.std_error == "std_error_error_modifier_0"
    check_sideeffects(test_agent, TEST_OUT_MODIFIER_FAIL)


@pytest.mark.skip(reason="Need to update this test to suit new agent.")
def test_agent_checker_fail():
    """
    Test agent on file containing checker_0 error.
    """
    test_agent = AgentMockCheckerFail()
    TEST_OUT_CHECKER_FAIL = CallsTruth(
        count=4,
        order=["syntax", "modifier_0", "modifier_1", "checker_0"],
        arg="test_file.py",
    )
    result = test_agent()
    assert result.error
    assert result.std_out == "std_out_error_checker_0"
    assert result.std_error == "std_error_error_checker_0"
    check_sideeffects(test_agent, TEST_OUT_CHECKER_FAIL)


@pytest.mark.skip(reason="Need to update this test to suit new agent.")
def test_agent_no_fail():
    """
    Test agent on file containing no errors.
    """
    test_agent = AgentMock()
    TEST_OUT_NO_FAIL = CallsTruth(
        count=5,
        order=["syntax", "modifier_0", "modifier_1", "checker_0", "checker_1"],
        arg="test_file.py",
    )
    assert (
        test_agent() is None
    ), "If no errors occur agent should not return anything. No news is good news."
    check_sideeffects(test_agent, TEST_OUT_NO_FAIL)
