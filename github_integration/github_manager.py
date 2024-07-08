"""
This module encapsulates functionalities for interacting with GitHub via the GitHub API. It provides a
set of features for managing GitHub data, including repositories, releases, issues, pull requests, and commits. The
GithubManager class, designed as a singleton, serves as the central point for all GitHub operations, ensuring efficient
and consistent access to the GitHub API. It also includes utilities for rate limit management and generating URLs for
change logs. This module is intended for applications that require direct interaction with GitHub data, offering both
fetch and store capabilities to streamline GitHub data management.
"""

import logging
import time

from datetime import datetime
from typing import Optional, Union

from github import Github
from github.GitRelease import GitRelease
from github.RateLimit import RateLimit
from github.Repository import Repository

from github_integration.model.commit import Commit
from github_integration.model.issue import Issue
from github_integration.model.pull_request import PullRequest


def singleton(cls):
    """
    A decorator for making a class a singleton.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class GithubManager:
    """
    A singleton class used to manage GitHub interactions.

    This class provides methods to fetch various GitHub objects such as repositories, releases, issues, pull requests,
    and commits.
    It maintains a persistent state for the GitHub connection, repository, and latest release information. Additionally,
    it offers static methods to output fetched data using the same methods without requiring an instance.
    """

    RATE_LIMIT_THRESHOLD_PERCENTAGE = 10  # Start sleeping logic when less than 10% of rate limit remains

    def __init__(self):
        self.__g = None
        self.__repository = None
        self.__git_release = None

    def reset(self) -> 'GithubManager':
        """
        Resets the GithubManager instance to its initial state.

        This method clears the current GitHub connection, repository, and latest release information,
        effectively resetting the instance to its initial state. This can be useful when needing to
        refresh the instance's state or switch to a different GitHub repository context.

        Returns:
            GithubManager: The instance itself after being reset, allowing for method chaining.
        """
        self.__g = None
        self.__repository = None
        self.__git_release = None
        return self

    @property
    def github(self) -> Github:
        """
        Gets the g attribute.

        :return: The Github object.
        """
        return self.__g

    @github.setter
    def github(self, g: Github):
        """
        Sets the g attribute.

        :return: The Github object.
        """
        self.__g = g

    @property
    def repository(self) -> Optional[Repository]:
        """
        Gets the repository attribute.

        :return: The Repository object, or None if it is not set.
        """
        return self.__repository

    @property
    def git_release(self) -> Optional[GitRelease]:
        """
        Gets the git_release attribute.

        :return: The GitRelease object, or None if it is not set.
        """
        return self.__git_release

    # store methods

    def store_repository(self, repository: Union[str, Repository] = None) -> 'GithubManager':
        """
        Fetches the latest release from the current repository or the provided one and stores it.

        :param repository: The repository to fetch the latest release from. Defaults to the current repository.
        :return: The GithubManager object.
        """
        if repository is not None and isinstance(repository, str):
            self.__repository = self.fetch_repository(repository)
        elif repository is not None and isinstance(repository, Repository):
            self.__repository = repository
        else:
            raise TypeError("Store repository failed. Repository must be a string or a Repository object")
        return self

    def store_latest_release(self, repository: Repository = None) -> 'GithubManager':
        """
        Fetches the latest release from the current repository or the provided one and stores it.

        :param repository: The repository to fetch the latest release from. Defaults to the current repository.
        :return: The GithubManager object.
        """
        self.__git_release = self.fetch_latest_release(repository)
        return self

    # fetch methods

    def fetch_repository(self, repository_id: str) -> Optional[Repository]:
        """
        Fetches a repository from GitHub using the provided repository ID.

        :param repository_id: The ID of the repository to fetch.
        :return: The fetched Repository object, or None if the repository could not be fetched.
        """
        try:
            logging.info("Fetching repository: %s", repository_id)
            return self.__g.get_repo(repository_id)
        except Exception as e:
            if "Not Found" in str(e):
                logging.error("Repository not found: %s", repository_id)
            else:
                logging.error("Fetching repository failed for %s: %s", repository_id, str(e))

        return None

    def fetch_latest_release(self, repository: Repository = None) -> Optional[GitRelease]:
        """
        Fetches the latest release from the specified repository or the current repository.

        :param repository: The repository to fetch the latest release from. Defaults to the current repository.
        :return: The fetched GitRelease object, or None if no release could be fetched.
        """
        if not repository and not self.__repository:
            logging.error("Fetching latest release failed. Repository is not set.")
            return None

        repo = repository or self.__repository

        try:
            logging.info("Fetching latest release for %s", repo.full_name)
            release = repo.get_latest_release()
            logging.debug("Found latest release: %s, created at: %s, published at: %s",
                          release.tag_name, release.created_at, release.published_at)
            return release
        except Exception as e:
            if "Not Found" in str(e):
                logging.error("Latest release not found for %s. 1st release for repository!", repo.full_name)
            else:
                logging.error("Fetching latest release failed for %s: %s. Expected first release for repository.",
                              repo.full_name, str(e))

        return None

    def fetch_issue(self, issue_number: int, repository: Repository = None) -> Optional[Issue]:
        """
        Fetches an issue from the specified repository or the current repository by its number.

        :param issue_number: The number of the issue to fetch.
        :param repository: The repository to fetch the issue from. Defaults to the current repository.
        :return: The fetched Issue object, or None if the issue could not be fetched.
        """
        if not repository and not self.__repository:
            logging.error("Fetching issue failed. Repository is not set.")
            return None

        repo = repository or self.__repository

        try:
            logging.info("Fetching issue number: %s", issue_number)
            issue = repo.get_issue(issue_number)
            logging.debug("Fetched issue: %s", issue.title)
            return Issue(issue)
        except Exception as e:
            logging.error("Fetching issue failed for issue number %s: %s", issue_number, str(e))
            return None

    def fetch_issues(self, since: Optional[datetime] = None, state: Optional[str] = None,
                     repository: Repository = None) -> list[Issue]:
        """
        Fetches issues from the specified repository or the current repository.

        :param since: The datetime to fetch issues since. If None, fetches issues since the repository's creation.
        :param state: The state of the issues to fetch (e.g., 'open', 'closed', 'all'). Defaults to 'all'.
        :param repository: The repository to fetch issues from. Defaults to the current repository.
        :return: A list of Issue objects.
        """
        if not repository and not self.__repository:
            logging.error("Fetching all issues failed. Repository is not set.")
            return []

        repo = repository or self.__repository

        if since is None:
            since = self.__get_since(repo)

        try:
            logging.info("Fetching all issues for %s since %s", repo.full_name, since)
            issues = repo.get_issues(state=state or "all", since=since)
            parsed_issues = [Issue(issue) for issue in issues]
            logging.info("Found %s issues for %s", len(parsed_issues), repo.full_name)
            return parsed_issues
        except Exception as e:
            logging.error("Fetching issues failed: %s", str(e))
            return []

    def fetch_pull_requests(self, since: datetime = None, repository: Repository = None) -> list[PullRequest]:
        """
        Fetches all pull requests from the specified repository or the current repository.

        :param since: The datetime to fetch pull requests since. If None, fetches all pull requests.
        :param repository: The repository to fetch pull requests from. Defaults to the current repository.
        :return: A list of PullRequest objects.
        """
        if not repository and not self.__repository:
            logging.error("Fetching all closed PRs failed. Repository is not set.")
            return []

        repo = repository or self.__repository

        logging.info("Fetching all closed PRs for %s", repo.full_name)
        pulls = repo.get_pulls(state="closed")

        pull_requests = []
        logging.info("Found %s PRs for %s", len(list(pulls)), repo.full_name)
        for pull in list(pulls):
            pull_requests.append(PullRequest(pull))

        return pull_requests

    def fetch_commits(self, since: datetime = None, repository: Repository = None) -> list[Commit]:
        """
        Fetches all commits from the specified repository or the current repository.

        :param since: The datetime to fetch commits since. If None, fetches all commits.
        :param repository: The repository to fetch commits from. Defaults to the current repository.
        :return: A list of Commit objects.
        """
        if not repository and not self.__repository:
            logging.error("Fetching all commits failed. Repository is not set.")
            return []

        repo = repository or self.__repository

        logging.info("Fetching all commits %s", repo.full_name)
        raw_commits = repo.get_commits()

        commits = []
        for raw_commit in raw_commits:
            # Note: kept for near future development
            #   - for reference commit author - use raw_commit.author
            commits.append(Commit(raw_commit))

        return commits

    # get methods

    def get_change_url(self, tag_name: str, repository: Repository = None, git_release: GitRelease = None) -> str:
        """
        Generates a URL for viewing changes associated with a given tag name in a GitHub repository.

        :param tag_name: The tag name for which the change URL is to be generated.
        :param repository: An optional Repository. If given, this repository is used instead current one.
        :param git_release: An Optional GitRelease. If given, URL compares this release with the tag name.
        :return: A string containing the URL to view the changes. Returns an empty string if the repository is not set.
        """
        if not repository and not self.__repository:
            logging.error("Get change url failed. Repository is not set.")
            return ""

        repo = repository or self.__repository
        rls = git_release or self.__git_release

        if rls is None:
            # If there is no latest release, create a URL pointing to all commits
            changelog_url = f"https://github.com/{repo.full_name}/commits/{tag_name}"
        else:
            # If there is a latest release, create a URL pointing to commits since the latest release
            changelog_url = f"https://github.com/{repo.full_name}/compare/{rls.tag_name}...{tag_name}"

        return changelog_url

    def get_repository_full_name(self) -> Optional[str]:
        """
        Gets the full name of the repository.

        :return: The full name of the repository as a string, or None if the repository is not set.
        """
        return self.__repository.full_name if self.__repository else None

    # others

    def show_rate_limit(self) -> 'GithubManager':
        """
        Shows the current rate limit and sleeps if the rate limit is reached.
        """
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            # save API Call when not in debug mode
            return self

        if self.__g is None:
            logging.error("Show Rate Limit failed. GitHub object is not set.")
            return self

        try:
            rate_limit: RateLimit = self.__g.get_rate_limit()

            threshold = rate_limit.core.limit * self.RATE_LIMIT_THRESHOLD_PERCENTAGE / 100
            if rate_limit.core.remaining < threshold:
                reset_time = rate_limit.core.reset
                sleep_time = (reset_time - datetime.utcnow()).total_seconds() + 10
                logging.debug("Rate limit reached. Sleeping for %s seconds.", sleep_time)
                time.sleep(sleep_time)
            else:
                logging.debug("Rate limit: %s remaining of %s", rate_limit.core.remaining, rate_limit.core.limit)
        except Exception as e:
            logging.error("Failed to get rate limit: %s", str(e))

    def __get_since(self, repository: Repository = None, git_release: GitRelease = None) -> Optional[datetime]:
        """
        Gets the 'since' datetime for fetching issues, pull requests, and commits.

        :param repository: The repository to use for determining the 'since' datetime. Default use current repository.
        :param git_release: The GitRelease to use for determining the 'since' datetime. Default use current git release.
        :return: The 'since' datetime, or None if it is not set.
        """
        if not repository and not self.__repository:
            logging.error("Get since failed. Repository is not set.")
            return None

        repo = repository or self.__repository

        if not git_release and not self.__git_release:
            return repo.created_at

        rls = git_release or self.__git_release

        return rls.published_at if rls.published_at else rls.created_at
