from datetime import datetime
from unittest.mock import Mock

from github_integration.model.pull_request import PullRequest


mock_commit1 = Mock()
mock_commit1.sha = "sha1"
mock_commit1.message = "Initial commit"
mock_commit2 = Mock()
mock_commit2.sha = "sha2"
mock_commit2.message = "Second commit"

# Create a mock GitPullRequest object
mock_git_pull_request = Mock()
mock_git_pull_request.id = 1
mock_git_pull_request.number = 42
mock_git_pull_request.title = "Test Pull Request"
mock_git_pull_request.body = "This is a test pull request. Fixes #123"
mock_git_pull_request.state = "open"
mock_git_pull_request.created_at = datetime(2023, 1, 1, 12, 0, 0)
mock_git_pull_request.updated_at = datetime(2023, 1, 2, 12, 0, 0)
mock_git_pull_request.closed_at = None
mock_git_pull_request.merged_at = None
mock_git_pull_request.assignee = Mock()
mock_git_pull_request.assignee.login = "octocat"
mock_git_pull_request.merge_commit_sha = "def456"

# Create mock labels
mock_label_bug = Mock()
mock_label_bug.name = "bug"
mock_label_enhancement = Mock()
mock_label_enhancement.name = "enhancement"

mock_git_pull_request.get_labels.return_value = [mock_label_bug, mock_label_enhancement]
pull_request = PullRequest(mock_git_pull_request)


def test_pull_request_id():
    assert 1 == pull_request.id


def test_pull_request_number():
    assert 42 == pull_request.number


def test_pull_request_title():
    assert "Test Pull Request" == pull_request.title


def test_pull_request_body():
    assert "This is a test pull request. Fixes #123" == pull_request.body


def test_pull_request_body_empty():
    mock_git_pull_request.body = None
    pull_request_with_empty_body = PullRequest(mock_git_pull_request)
    assert "" == pull_request_with_empty_body.body


def test_pull_request_state():
    assert "open" == pull_request.state


def test_pull_request_created_at():
    assert datetime(2023, 1, 1, 12, 0, 0) == pull_request.created_at


def test_pull_request_updated_at():
    assert datetime(2023, 1, 2, 12, 0, 0) == pull_request.updated_at


def test_pull_request_closed_at():
    assert pull_request.closed_at is None


def test_pull_request_merged_at():
    assert pull_request.merged_at is None


def test_pull_request_assignee():
    assert "octocat" == pull_request.assignee


def test_pull_request_labels():
    labels = [label.name for label in mock_git_pull_request.get_labels()]
    assert pull_request.labels == labels


def test_pull_request_is_merged():
    assert not pull_request.is_merged


def test_pull_request_is_closed():
    assert not pull_request.is_closed


def test_pull_request_body_contains_issue_mention():
    assert pull_request.body_contains_issue_mention


def test_pull_request_author():
    assert pull_request.author is None


def test_pull_request_contributors():
    assert [] == pull_request.contributors


def test_pull_request_merge_commit_sha():
    assert "def456" == pull_request.merge_commit_sha


def test_pull_request_mentioned_issues():
    assert [123] == pull_request.mentioned_issues


def test_pull_request_contains_labels():
    assert pull_request.contains_labels(["bug"])
    assert not pull_request.contains_labels(["nonexistent_label"])


def test_register_commit_and_commit_count():
    assert pull_request.commits_count() == 0

    pull_request.register_commit(mock_commit1)
    pull_request.register_commit(mock_commit2)

    assert pull_request.commits_count() == 2
