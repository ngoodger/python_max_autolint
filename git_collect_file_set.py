from git import Repo
import os


class GitCollectFileSet:
    def __init__(self, working_tree_dir):
        """
        Args:
            working_tree_dir (str): project root folder containing .git
        """
        self.repo = Repo(working_tree_dir)

    def __call__(self):
        """
        Description:
            collect changed files in project.
        Returns:
            files (List[str]): List of full path files that are staged for commit. 
        """
        diffs = self.repo.index.diff(self.repo.head.commit)
        files = [os.path.join(self.repo.working_dir, diff.a_path) for diff in diffs]
        return files


class GitCollectTrackedFileSet:
    def __init__(self, working_tree_dir):
        """
        Args:
            working_tree_dir (str): project root folder containing .git
        """
        self.repo = Repo(working_tree_dir)

    def __call__(self):
        """
        Description:
            collect changed files in project.
        Returns:
            files (List[str]): List of full path files that are staged for commit. 
        """
        tracked_files = {
            blob.abspath for blob in self.repo.heads.master.commit.tree.blobs
        }
        # Filter files with .py extension
        py_extension_files = {file for file in tracked_files if file[-3:] == ".py"}
        print(py_extension_files)
        # Find files with python shebang
        non_py_extension_files = tracked_files - py_extension_files
        py_shebang_files = []
        for file in non_py_extension_files:
            with open(file, "r") as f:
                first_line = f.readline()
                # Check for python shebang.
                if "python" in first_line:
                    py_shebang_files.append(file)
        return list(py_extension_files) + py_shebang_files
