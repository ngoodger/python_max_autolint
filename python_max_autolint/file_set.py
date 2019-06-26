import logging
from typing import List

logger = logging.getLogger(__name__)


class FileSet:
    """
    Applies operations to files and rotects files from invalid operations.
    """

    def __init__(self, files: List[str], ops_set):
        self.ops_set = ops_set
        self.files = files
        self.finished = False
        self.locked = False

    def update(self, op=None):

        if op is not None:
            # Only run op if:
            # 1. file_set not locked already by running op.
            # 2. op not already running
            running_ops = (
                self.ops_set.modifying_running_ops | self.ops_set.checking_running_ops
            )
            if not self.locked and ((op not in running_ops)):
                # Locking operation should lock the fileset to prevent any other ops from running.
                if op.modifying:
                    self.locked = True
                    self.ops_set.modifying_running_ops.add(op)
                else:
                    self.ops_set.checking_running_ops.add(op)
                op(self.files)

        # Copy running_ops set to list to avoid changing size while iterating through each op.
        running_ops_temp = list(
            self.ops_set.modifying_running_ops | self.ops_set.checking_running_ops
        )
        # Check state
        for op in running_ops_temp:
            if op.check_done():
                # If op was modifying it must have locked the fileset and can unlock it again since it is complete.
                if op.modifying:
                    self.locked = False
                    self.ops_set.modifying_finished_ops.add(op)
                    self.ops_set.modifying_running_ops.remove(op)
                else:
                    self.ops_set.checking_finished_ops.add(op)
                    self.ops_set.checking_running_ops.remove(op)

    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return str(self.files)
