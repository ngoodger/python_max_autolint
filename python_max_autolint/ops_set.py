import inspect
from python_max_autolint import ops, file_operator


class OpsSet:
    def __init__(self):
        # Get all operator classes from ops module.
        OpClasses = [
            op_tuple[1] for op_tuple in inspect.getmembers(ops, inspect.isclass)
        ]

        self.ops = set()
        self.checking_ops = set()
        self.modifying_ops = set()
        self.modifying_finished_ops = set()
        self.modifying_running_ops = set()
        self.checking_running_ops = set()
        self.checking_finished_ops = set()
        self.map_modifying_checking = {}
        self.map_checking_modifying = {}
        for OpClass in OpClasses:
            op_obj = OpClass()
            self.ops.add(op_obj)
            if op_obj.modifying:
                self.modifying_ops.add(op_obj)
            else:
                self.checking_ops.add(op_obj)
        for modify_op in self.modifying_ops:
            self.map_modifying_checking[modify_op] = None
            for check_op in self.checking_ops:
                if modify_op.tool_name == check_op.tool_name:
                    self.map_modifying_checking[modify_op] = check_op
            assert (
                self.map_modifying_checking[modify_op] is not None
            ), "For each modifying op there must exist a checking op"
        for check_op in self.checking_ops:
            self.map_checking_modifying[check_op] = None
            for modify_op in self.modifying_ops:
                if check_op.tool_name == modify_op.tool_name:
                    self.map_checking_modifying[check_op] = modify_op
