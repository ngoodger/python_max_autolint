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
