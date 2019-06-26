import time
import logging

logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, file_set, agent, monitor):
        self.file_set = file_set
        self.agent = agent
        self.monitor = monitor

    def __call__(self):
        # Only run tools if there is actually something to run them on.
        if len(self.file_set) == 0:
            logger.debug("No files to check.")
            return

        while True:
            action = self.agent.choose_action()
            logger.debug(f"Action: {action}")
            self.file_set.update(action)
            if self.monitor.check_finished():
                break
            time.sleep(0.01)
        return self.monitor.result
        # file_set.report(self.ops)
