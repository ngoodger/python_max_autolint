import agent
import time
import math

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
    
