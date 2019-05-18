from git_collect_file_set GitCollectFileSet
import unittest.mock as mock 


@pytest.fixture
def git_project(tmp_path):
    

class TestGitCollectFileSet():
    path = ""
    TEST_TYPE= "unit"
    if TEST_TYPE == "unit":
        test_collect_file_set = GitCollectFileSet(path="") 
