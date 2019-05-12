import agent
import time
import math
from unittest.mock import Mock, Mock
from agent import ReturnCode

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
    
def test_call():
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

    test_agent = AgentMock()
    test_agent()

    # Check all components called in order.
    assert(len(test_agent.parent_mock.mock_calls) == 5), "All checks should be done"
    assert(test_agent.parent_mock.mock_calls[0][0] == "syntax")
    assert(test_agent.parent_mock.mock_calls[1][0] == "modifier_0")
    assert(test_agent.parent_mock.mock_calls[2][0] == "modifier_1")
    assert(test_agent.parent_mock.mock_calls[3][0] == "checker_0")
    assert(test_agent.parent_mock.mock_calls[4][0] == "checker_1")

    # Check all components called with correct argument.
    test_agent.syntax.assert_called_once_with("test_file.py")
    test_agent.modifiers[0].assert_called_once_with("test_file.py")
    test_agent.modifiers[1].assert_called_once_with("test_file.py")
    test_agent.checkers[0].assert_called_once_with("test_file.py")
    test_agent.checkers[1].assert_called_once_with("test_file.py")

