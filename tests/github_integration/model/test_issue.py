from datetime import datetime

from github_integration.model.issue import Issue


class MockGitIssue:
    def __init__(self, id, number, title, body, state, created_at, state_reason, labels):
        self.id = id
        self.number = number
        self.title = title
        self.body = body
        self.state = state
        self.created_at = created_at
        self.state_reason = state_reason
        self._labels = labels

    def get_labels(self):
        return self._labels


class MockLabel:
    def __init__(self, name):
        self.name = name


# Create a mock GitIssue object
mock_git_issue = MockGitIssue(
    id=1,
    number=42,
    title="Test Issue",
    body="This is a test issue.",
    state="open",
    created_at=datetime(2023, 1, 1, 12, 0, 0),
    state_reason="open reason",
    labels=[MockLabel("bug"), MockLabel("enhancement")]
)

issue = Issue(mock_git_issue)


def test_issue_id():
    assert 1 == issue.id


def test_issue_number():
    assert 42 == issue.number


def test_issue_title():
    assert "Test Issue" == issue.title


def test_issue_body():
    assert "This is a test issue." == issue.body


def test_issue_body_empty():
    empty_body_issue = MockGitIssue(
        id=1,
        number=42,
        title="Test Issue",
        body=None,
        state="open",
        created_at=datetime(2023, 1, 1, 12, 0, 0),
        state_reason="open reason",
        labels=[MockLabel("bug"), MockLabel("enhancement")]
    )
    issue_with_empty_body = Issue(empty_body_issue)
    assert "" == issue_with_empty_body.body


def test_issue_state():
    assert "open" == issue.state


def test_issue_labels():
    assert ["bug", "enhancement"] == issue.labels


def test_issue_created_at():
    assert datetime(2023, 1, 1, 12, 0, 0) == issue.created_at


def test_issue_state_reason():
    assert "open reason" == issue.state_reason


def test_issue_is_closed():
    assert not issue.is_closed()
    closed_issue = MockGitIssue(
        id=1,
        number=42,
        title="Test Issue",
        body="This is a test issue.",
        state="closed",
        created_at=datetime(2023, 1, 1, 12, 0, 0),
        state_reason="closed reason",
        labels=[MockLabel("bug"), MockLabel("enhancement")]
    )
    closed_issue_instance = Issue(closed_issue)
    assert closed_issue_instance.is_closed()


def test_issue_contains_labels():
    assert issue.contains_labels(["bug"])
    assert not issue.contains_labels(["nonexistent_label"])
