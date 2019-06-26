import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

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

    def __init__(self, ops_set):
        self.ops_set = ops_set

    @abstractmethod
    def choose_action(self):
        pass


class ModifiersFirstAgent(Agent):
    def choose_action(self):

        # Determine which modifiers and which checkers are yet to be started.
        modifying_running_and_finished_ops = (
            self.ops_set.modifying_running_ops | self.ops_set.modifying_finished_ops
        )
        unstarted_modifying_ops = (
            self.ops_set.modifying_ops - modifying_running_and_finished_ops
        )
        checking_running_and_finished_ops = (
            self.ops_set.checking_running_ops | self.ops_set.checking_finished_ops
        )
        unstarted_checking_ops = (
            self.ops_set.checking_ops - checking_running_and_finished_ops
        )

        # Choose action based on running unstarted modifiers first.  After that run unstarted checkers.
        if len(unstarted_modifying_ops) > 0:
            return unstarted_modifying_ops.pop()
        elif len(unstarted_checking_ops) > 0:
            return unstarted_checking_ops.pop()
        else:
            return None
