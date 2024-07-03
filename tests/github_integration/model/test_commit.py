from datetime import datetime

from github_integration.model.commit import Commit


class MockGitCommit:
    def __init__(self, sha, message, author_login):
        self.sha = sha
        self.commit = self
        self.message = message
        self.author = self
        self.login = author_login


# Create a mock GitCommit object
mock_git_commit = MockGitCommit(
    sha="abc123",
    message="Initial commit",
    author_login="octocat"
)

commit = Commit(mock_git_commit)


def test_commit_sha():
    assert commit.sha == "abc123"


def test_commit_message():
    assert commit.message == "Initial commit"


def test_commit_author():
    assert commit.author == "octocat"
