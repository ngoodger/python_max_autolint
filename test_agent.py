from dataclasses import dataclass
import agent
import time
import math
from unittest.mock import Mock, Mock
from agent import ReturnCode
import pytest

def test_timeit():
    SLEEP_MS = 2
    MS_IN_SECOND = 1000
    ERROR_VALUE = "test return value"
    def test_function():
        time.sleep(SLEEP_MS / MS_IN_SECOND)
        return ERROR_VALUE
    
    timed_test_function = agent.Agent.timeit(test_function)
    return_test = timed_test_function()
    assert(return_test.error == ERROR_VALUE)
    # Test time in milliseconds should always be 1 over SLEEP_MS because of function overhead
    # and ceiling function is used to round up.
    assert(math.isclose(return_test.elapsed_time_ms, SLEEP_MS + 1))

@dataclass
class CallsTruth:
    count: int
    order: list
    arg: str 
    
@pytest.fixture
def TestAgentClass():
    class AgentMock(agent.Agent):
        # Override init function to replace components with mocks
        def __init__(self):
            self.file_collector = Mock(return_value="test_file.py") 
            return_code = ReturnCode(error=None, elapsed_time_ms=100)
            self.parent_mock = Mock(return_value=return_code) 
            self.parent_mock.syntax = Mock(return_value=return_code) 
            self.parent_mock.modifier_0 = Mock(return_value=return_code)  
            self.parent_mock.modifier_1 = Mock(return_value=return_code)
            self.parent_mock.checker_0 = Mock(return_value=return_code)
            self.parent_mock.checker_1 = Mock(return_value=return_code)
            self.syntax = self.parent_mock.syntax 
            self.modifiers= [self.parent_mock.modifier_0, self.parent_mock.modifier_1]
            self.checkers = [self.parent_mock.checker_0, self.parent_mock.checker_1]
    return AgentMock

TEST_OUT_NO_FAIL = (CallsTruth(count= 5, order=["syntax", "modifier_0", "modifier_1", "checker_0", "checker_1"],
                                arg = "test_file.py"))
TEST_OUT_SYNTAX_FAIL = (CallsTruth(count= 1, order=["syntax"],
                                arg = "test_file.py"))
TEST_OUT_MODIFIER_FAIL = (CallsTruth(count= 2, order=["syntax", "modifier_0"],
                                arg = "test_file.py"))
TEST_OUT_CHECKER_FAIL = (CallsTruth(count= 4, order=["syntax", "modifier_0", "modifier_1", "checker_0"],
                                arg = "test_file.py"))

results = ["test_input, expected", [("no_fail", TEST_OUT_NO_FAIL),
                                       ("syntax_fail", TEST_OUT_SYNTAX_FAIL),
                                       ("modifier_fail", TEST_OUT_MODIFIER_FAIL),
                                       ("checker_fail", TEST_OUT_CHECKER_FAIL),]]

#@pytest.mark.usefixtures("TestAgentClass")
@pytest.mark.parametrize(*results)
def test_my_agent(TestAgentClass, test_input, expected):
    if test_input == "no_fail":
        class TestAgentNewClass(TestAgentClass):
            pass
    elif test_input == "syntax_fail":
        class TestAgentNewClass(TestAgentClass):
            def __init__(self):
                super(TestAgentNewClass, self).__init__()
                self.parent_mock.syntax.return_value = ReturnCode(error="fail", elapsed_time_ms=10) 
    elif test_input == "modifier_fail":
        class TestAgentNewClass(TestAgentClass):
            def __init__(self):
                super(TestAgentNewClass, self).__init__()
                self.parent_mock.modifier_0.return_value = ReturnCode(error="fail", elapsed_time_ms=10) 
    elif test_input == "checker_fail":
        class TestAgentNewClass(TestAgentClass):
            def __init__(self):
                super(TestAgentNewClass, self).__init__()
                self.parent_mock.checker_0.return_value = ReturnCode(error="fail", elapsed_time_ms=10) 
    else:
        raise NotImplmenetedError
    test_agent = TestAgentNewClass()
    # Call test agent.
    test_agent()
    assert(len(test_agent.parent_mock.mock_calls) == expected.count), "All checks should be done"
    # Check call order is correct and calls occur with correct args.
    for i, call in enumerate(expected.order):
        call == test_agent.parent_mock.mock_calls[i][0] 
        expected.arg == test_agent.parent_mock.mock_calls[i][1] 

results = ["test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)]]
@pytest.mark.parametrize(*results)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
