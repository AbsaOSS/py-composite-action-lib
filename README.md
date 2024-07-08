# PyCompositeActionLib

- [Description](#description)
- [Motivation](#motivation)
- [How to Use](#how-to-use)
  - [Example: Control Action Inputs and Outputs](#example-control-action-inputs-and-outputs)
  - [Example: Access GitHub API with GithubManager](#example-access-github-api-with-githubmanager)
- [Features](#features)
- [How to Use Local Version of Library for Development](#how-to-use-local-version-of-library-for-development)
- [How to Run Tests](#how-to-run-tests)
- [How to Run Code Check](#how-to-run-code-check)
- [How to Release](#how-to-release)
- [Contribution Guidelines](#contribution-guidelines)
- [License Information](#license-information)
- [Contact or Support Information](#contact-or-support-information)


## Description
**PyCompositeActionLib** is a Python library that streamlines creating and managing composite GitHub Actions. It offers reusable classes and scripts for controlling action inputs/outputs and accessing the GitHub API. 

## Motivation
The motivation behind PyCompositeActionLib is to provide developers with a robust set of tools that simplify the creation of composite GitHub Actions. By leveraging reusable components and streamlined API access, this library aims to reduce redundancy, improve efficiency, and enhance the overall development experience for creating complex workflows on GitHub.

## How to use
### Example: Control Action Inputs and Outputs
```python
from py_composite_action_lib import get_action_input, set_action_output, set_action_failed

# Example: Get action input
repo_name = get_action_input('repo-name')
if not repo_name:
    set_action_failed('The input "repo-name" is required.')

# Example: Set action output
set_action_output('output-name', 'success')
```

### Example: Access GitHub API with GithubManager
```python
from github import Github, Auth
from py_composite_action_lib import GithubManager

# Authenticate to GitHub
token = 'your_github_token'
auth = Auth.Token(token=token)   
GithubManager().github = Github(auth=auth)

# Fetch a repository
repo = GithubManager().fetch_repository('owner/repo')
if repo:
    print(f'Repo name: {repo.full_name}')
else:
    GithubManager().set_action_failed('Failed to fetch repository.')

# Fetch the latest release
latest_release = GithubManager().fetch_latest_release()
if latest_release:
    print(f'Latest release: {latest_release.tag_name}')
else:
    print('No releases found.')

# Fetch an issue
issue_number = 1
issue = GithubManager().fetch_issue(issue_number)
if issue:
    print(f'Issue title: {issue.title}')
else:
    print(f'Issue #{issue_number} not found.')
```

## Features
- **Control Action Inputs and Outputs**: Manage and validate action parameters with ease.
- **GitHub API Integration**: Seamlessly interact with GitHub’s API for various operations such as repositories, issues, releases, and more.
- **Reusable Components**: Write once, reuse across multiple actions to save time and effort.

## How to install for development
1. To use your library in development mode, you need to install it using the pip tool with the -e option. Navigate to the directory containing your setup.py and run:
```bash
cd path/to/PyCompositeActionLib
pip install -e .

**Optional**: If you want to install development dependencies (e.g., for testing), you can include them in the installation command:
pip install -e .[dev]
```
Hint: The -e option stands for "editable," meaning any changes you make to the library code will immediately be reflected in the environment.
2. Now you can use your library in your other Python projects. For example, in your project directory:
```python
from mylibrary.module1 import some_function

some_function()
```
TODO - improve the example above

## How to run tests
To run tests for PyCompositeActionLib, use the following commands:
- Ensure you are in the project directory and have the virtual environment activated.
- Install test dependencies:
```bash
pip install -r requirements-test.txt
```
- Set the PYTHONPATH environment variable to the project root directory:
```bash
export PYTHONPATH={path-to-your-project}/py-composite-action-lib
```
- See `pytest` configuration in `pytest.ini` file for defined test markers:
```bash
[pytest]
markers =
    integration: marks integration tests
```
### Run all tests using pytest (from project root):
- Run all tests:
```bash
pytest
```
- Run all tests with code coverage:
```bash
pytest --cov=action --cov=github_integration --cov-report html tests/ -vv
```

### Run separated unit and integration tests using pytest (from project root):
Note: unit tests are all tests without the `integration` marker.
```bash
pytest -m "not integration"
pytest -m integration
```
- Run selection of tests with code coverage:
```bash
pytest --cov=action --cov=github_integration --cov-report html -m "not integration" tests/ -vv
pytest --cov=action --cov=github_integration --cov-report html -m integration tests/ -vv
```

## How to run code check
- Install pylint
```bash
pip install pylint
```
- Configure pylint
```bash
pylint --generate-rcfile > .pylintrc
```
- Run pylint
```bash
pylint ./py-composite-action-lib/src
```


## How to release
### Update `setup.py`
- Edit the file content with all necessary changes.

### Create Distribution Files
- Use setuptools and wheel to create distribution files. First, ensure these packages are installed:
```bash
pip install setuptools wheel
```
- Run from the project root directory:
```bash
python setup.py sdist bdist_wheel
```
- This will create the following files in a dist/ directory:
  - A source archive (.tar.gz)
  - A built distribution (.whl)
  
### Upload to PyPI
- If not registered, create an account on PyPI.
- Install twine to securely upload the distribution files:
```bash
pip install twine
```
- Upload Your Package:
```bash
twine upload dist/*
```
  - **You will be prompted to enter your PyPI username and password.**

### Verify the Upload
- Once uploaded, you can verify that your package is available on PyPI by visiting: https://pypi.org/project/mylibrary/
TODO - customize the link above

### Install Your Library
- To ensure everything works as expected, try installing your library from PyPI in a clean environment:
```bash
pip install mylibrary
```

### Tagging the Release in Git
```sbt
git tag v0.1.0
git push origin v0.1.0
```

### Contribution Guidelines

We welcome contributions to the PyCompositeActionLib! Whether you're fixing bugs, improving documentation, or proposing new features, your help is appreciated.

#### How to Contribute
- **Submit Pull Requests**: Feel free to fork the repository, make changes, and submit a pull request. Please ensure your code adheres to the existing style and all tests pass.
- **Report Issues**: If you encounter any bugs or issues, please report them via the repository's [Issues page](https://github.com/AbsaOSS/py-composite-action-lib/issues).
- **Suggest Enhancements**: Have ideas on how to make this action better? Open an issue to suggest enhancements.

Before contributing, please review our [contribution guidelines](https://github.com/AbsaOSS/py-composite-action-lib/blob/master/CONTRIBUTING.md) for more detailed information.

### License Information

This project is licensed under the Apache License 2.0. It is a liberal license that allows you great freedom in using, modifying, and distributing this software, while also providing an express grant of patent rights from contributors to users.

For more details, see the [LICENSE](https://github.com/AbsaOSS/py-composite-action-lib/blob/master/LICENSE) file in the repository.

### Contact or Support Information

If you need help with using or contributing to Generate Release Notes Action, or if you have any questions or feedback, don't hesitate to reach out:

- **Issue Tracker**: For technical issues or feature requests, use the [GitHub Issues page](https://github.com/AbsaOSS/py-composite-action-lib/issues).
- **Discussion Forum**: For general questions and discussions, join our [GitHub Discussions forum](https://github.com/AbsaOSS/py-composite-action-lib/discussions).
