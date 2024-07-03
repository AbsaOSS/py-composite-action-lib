import os
import sys


def get_action_input(name: str) -> str:
    """
    Retrieve the value of a specified input parameter from environment variables.

    This function constructs the environment variable name by replacing hyphens with
    underscores, converting the string to uppercase, and prefixing it with 'INPUT_'.
    It then retrieves the value of this environment variable.

    Args:
        name (str): The name of the input parameter.

    Returns:
        str: The value of the specified input parameter, or an empty string if the environment
        variable is not set.
    """
    return os.getenv(f'INPUT_{name.replace("-", "_").upper()}', '')


def set_action_output(name: str, value: str, default_output_path: str = "default_output.txt"):
    """
    Write an action output to a file in the format expected by GitHub Actions.

    This function writes the output in a specific format that includes the name of the
    output and its value. The output is appended to the specified file.

    Args:
        name (str): The name of the output parameter.
        value (str): The value of the output parameter.
        default_output_path (str, optional): The default file path to which the output is
        written if the 'GITHUB_OUTPUT' environment variable is not set. Defaults to "default_output.txt".
    """
    output_file = os.getenv('GITHUB_OUTPUT', default_output_path)
    with open(output_file, 'a') as f:
        f.write(f"{name}<<EOF\n")
        f.write(f"{value}")
        f.write(f"EOF\n")


def set_action_failed(message: str):
    """
    Mark the GitHub Action as failed and exit with an error message.

    This function prints an error message in the format expected by GitHub Actions
    and then exits the script with a non-zero status code.

    Args:
        message (str): The error message to be displayed.
    """
    print(f'::error::{message}')
    sys.exit(1)
