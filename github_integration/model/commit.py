"""
This module defines the Commit class, which represents a commit in GitHub. It encapsulates the data and operations
related to a GitHub commit, such as retrieving commit details (SHA, message, author). The Commit class provides a
structured way to access commit information, making it easier to integrate GitHub commit data into applications or
scripts that require detailed commit information. This module is part of a larger system designed to interact with
GitHub, focusing on commit management within the context of GitHub integration.
"""

from github import Commit as GitCommit


class Commit:
    """
    A class used to represent a commit in GitHub.
    """

    def __init__(self, commit: GitCommit):
        """
        Constructs all the necessary attributes for the Commit object.

        :param commit: The GitCommit object.
        """
        self.__commit: GitCommit = commit

    @property
    def sha(self) -> str:
        """
        Gets the SHA of the commit.

        :return: The SHA of the commit as a string.
        """
        return self.__commit.sha

    @property
    def message(self) -> str:
        """
        Gets the message of the commit.

        :return: The message of the commit as a string.
        """
        return self.__commit.commit.message

    @property
    def author(self) -> str:
        """
        Gets the author of the commit.

        :return: The author of the commit as a string.
        """
        return self.__commit.author.login
