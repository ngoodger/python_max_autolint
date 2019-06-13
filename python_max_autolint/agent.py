import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

from python_max_autolint import file_set

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class FileSet:
    files: list
    syntax_run: set
    checkers_run: set
    modifiers_run: set
    good: bool
    lock: bool


class Agent(ABC):
    """
    Orchestrates file set modification / checking.
    """

    def __init__(self, ops, file_set):
        self.file_set = file_set
        self.ops = ops

    def __call__(self):

        # Only run tools if there is actually something to run them on.
        if len(self.file_set) == 0:
            logger.debug("No files to check.")
            return

        while True:
            for op in self.ops:
                action = self.choose_action(self.observe())
                logger.debug(f"Action: {action}")
                self.file_set.update(action)
                if self.file_set.finished:
                    break
                time.sleep(0.01)
            if self.file_set.finished:
                break
        file_set.report(self.ops)

    def observe(self):
        observation = {
            "ops_to_run": self.file_set.ops_to_run,
            "running_ops": self.file_set.running_ops,
            "finished_ops": self.file_set.finished_ops,
        }
        return observation

    @abstractmethod
    def choose_action(self, observation):
        pass


class OrderedAgent(Agent):
    def choose_action(self, observation):
        ops_to_run = observation["ops_to_run"]
        running_ops = observation["running_ops"]
        finished_ops = observation["finished_ops"]
        non_running_or_finished_ops = ops_to_run - (running_ops | finished_ops)
        locking_ops = [op for op in non_running_or_finished_ops if op.locking]
        sorted_locking_ops = sorted(locking_ops, key=lambda x: x.reporting_priority)
        non_locking_ops = [op for op in non_running_or_finished_ops if not op.locking]
        sorted_non_locking_ops = sorted(
            non_locking_ops, key=lambda x: x.reporting_priority
        )
        if len(sorted_locking_ops) > 0:
            action = sorted_locking_ops[0]
        elif len(non_locking_ops):
            action = sorted_non_locking_ops[0]
        else:
            action = None
        return action
