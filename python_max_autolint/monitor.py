class Monitor:
    def __init__(self, ops_set):
        self.ops_set = ops_set
        self.result = None

    def check_finished(self):
        # Finish conditions
        # All checkers or modifiers finish success.
        finish = True
        # Compare each op to each other op.

        # Finished if all ops
        finished_ops = (
            self.ops_set.modifying_finished_ops | self.ops_set.checking_finished_ops
        )
        if finished_ops == self.ops_set.ops:
            for op in finished_ops:
                if op.result.error:
                    self.result = op.result
            return True
        else:
            return False


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
        # raise Exception
