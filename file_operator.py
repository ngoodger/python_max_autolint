class FileOperator(ABC):
    def __init__(self, files: List[str]):
        self.files = files

    def __call__(self):
        self.proc = sp.Popen(
            self.base_cmd + self.files,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            universal_newlines=True,
        )

    def done(self):
        proc_done = not self.proc.poll() is None
        # If process is finished update file properties according to stdout and stderr.
        if proc_done:
            self.std_out, self.std_err = self.proc.communicate(timeout=1)
            self.return_code = self.proc.returncode
            self.update_file_properties()
            self.err_update_file_properties(err)
            self.files[reformatted_filename].modifier_applied.add(type(self).__name__)
        return proc_done

    @property
    @abstractmethod
    def base_cmd(self):
        pass

    @property
    @abstractmethod
    def return_code_lookup(self):
        [0: SUCESS] 
        pass
