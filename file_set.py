import sys
from typing import List


class FileSet:
    """
    Manages state of files and Protects files from invalid operations.
    """

    def __init__(self, files: List[str], ops_to_run):
        self.files = files
        self.finished = False
        self.locked = False
        self.running_ops = set()
        self.finished_ops = set()
        self.ops_to_run = ops_to_run
        self.highest_reporting_priority = 99  # Lowest priorty.
        # Find highest reporting priority op.
        for op in ops_to_run:
            if op.reporting_priority < self.highest_reporting_priority:
                self.highest_reporting_priority = op.reporting_priority

    def update(self, ops=[]):
        for op in ops:
            # Only run op if:
            # 1. file_set not locked already by running op.
            # 2. op not already running or has already been run.
            # 3. op is not locking (can run concurrently) or there are no running ops so it is ok start and lock.
            # 4. ops that must be run first has not already finished or is not part of run.
            # 4. not already finished.
            if (
                not self.locked
                and op not in (self.running_ops or self.finished_ops)
                and (not op.locking or len(self.running_ops) == 0)
                and (
                    op.run_first.issubset({type(op) in self.finished_ops})
                    or not op.run_first.issubset({type(op) in self.ops_to_run})
                )
                and not self.finished
            ):
                # Locking operation should lock the fileset to prevent any other ops from running.
                if op.locking:
                    self.locked = True
                op(self.files)
                self.running_ops.add(op)

        # Copy running_ops set to list to avoid changing size while iterating through each op.
        running_ops_temp = list(self.running_ops)
        # Check state
        for op in running_ops_temp:
            if op.check_done():
                # If op was locking it must have locked the fileset and can unlock it again since it is complete.
                if op.locking:
                    self.locked = False
                self.running_ops.remove(op)
                self.finished_ops.add(op)

        self.check_finished()
        if self.finished:
            pass
            # TODO terminate ops.

    def check_finished(self):
        # Finished if no higher reporting priority op is yet to finish than one that already has an error.
        for op in self.finished_ops:
            if (
                op.result.error
                and self.highest_reporting_priority >= op.reporting_priority
            ):
                self.finished = True
        # Finished if all ope
        if self.finished_ops == self.ops_to_run:
            self.finished = True

    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return str(self.files)


def report(ops):
    error_op = None
    for op in ops:
        if op.result is not None and op.result.error:
            if error_op is None or error_op.reporting_priority > op.reporting_priority:
                error_op = op
    if error_op is not None:
        sys.stdout.write(f"{str(error_op)}\n")
        result = error_op.result
        sys.stdout.write(result.std_out)
        sys.stderr.write(result.std_error)
        raise Exception
