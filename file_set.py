import sys
from typing import List

class FileSet:
    """
    Manages state of files and Protects files from invalid operations. 
    """
    def __init__(self, files: List[str], ops_to_run):
        self.files = files
        self.good = False
        self.locked = False
        self.running_ops = set()
        self.finished_ops = set()
        self.ops_to_run = ops_to_run

    def update(self, ops=[]):
        for op in ops:
            # Only run op if:
            # 1. file_set not locked already by running op. 
            # 2. op not already running or has already been run.
            # 3. op is not locking (can run concurrently) or there are no running ops so it is ok start and lock. 
            if not self.locked and op not in (self.running_ops or self.finished_ops) and (not op.locking or len(self.running_ops) == 0):
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

    def check_finished(self):
        error_ops = [] 
        for op in self.finished_ops:
            if op.get_result().error:
                error_ops.append(op)
        for error_op in error_ops:
            result = error_op.get_result
            sys.stdout.write(result.std_out)
            sys.stderr.write(result.std_error)
            raise Exception
        if self.finished_ops == self.ops_to_run:
            self.good = True

    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return str(self.files)
