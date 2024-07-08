from setuptools import setup, find_packages

setup(
    name="PyCompositeActionLib",
    version="0.1.0",
    description="A Python library for composite actions.",
    author="Miroslav Pojer",
    author_email="miroslav.pojer@absa.africa",
    packages=find_packages(include=["action", "github_integration"]),
    install_requires=[
        "PyGithub>=1.59.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==5.0.0",
            "coverage==7.5.2",
            "pylint==3.2.5",
        ]
    },
)
