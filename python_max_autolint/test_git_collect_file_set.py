import pytest
from python_max_autolint import git_collect_file_set
import os
from git import Repo


@pytest.fixture
def repo_with_init_commit(tmp_path):
    repo = Repo.init(tmp_path, bare=False)
    empty_filename = os.path.join(tmp_path, "empty_file.txt")
    with open(empty_filename, "w") as f:
        f.write("")
    repo.index.add([empty_filename])
    repo.index.commit("Initial commit.")
    return tmp_path


@pytest.fixture
def repo_with_2_files_staged_for_commit(repo_with_init_commit):
    new_file0 = os.path.join(repo_with_init_commit, "new_file0.py")
    with open(new_file0, "w") as f:
        f.write("a = 1 + 2")
    new_file1 = os.path.join(repo_with_init_commit, "new_file1.py")
    with open(new_file1, "w") as f:
        f.write("b = 1 + 2")
    repo = Repo(repo_with_init_commit)
    repo.index.add([new_file0, new_file1])
    return repo_with_init_commit


def test_init(repo_with_init_commit):
    # Ensure no exceptions are raised on init.
    dut = git_collect_file_set.GitCollectFileSet(repo_with_init_commit)  # noqa F841


def test_collect_files(repo_with_2_files_staged_for_commit):
    dut = git_collect_file_set.GitCollectFileSet(repo_with_2_files_staged_for_commit)
    files = dut()
    assert "new_file0.py" in files[0], "new_file0.py should be staged for commit."
    assert "new_file1.py" in files[1], "new_file1.py should be staged for commit."
