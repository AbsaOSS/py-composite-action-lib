"""
This module defines the BaseActionInputs class, an abstract base class designed for handling action-specific variables
in a structured manner. It provides a framework for accessing and validating action-specific variables, which can be
either user-defined through environment variables or predefined as default values within child classes. The primary
purpose of this module is to standardize the process of managing action inputs across different actions, ensuring
consistent validation and access patterns.
"""

from abc import ABC, abstractmethod


class BaseActionInputs(ABC):
    """
    Abstract base class for classes that will access action-specific variables.

    This class serves as a parent for classes which will access action-specific
    variables defined in environment variables (user-defined) or defined by
    the child class as default values.
    """

    @staticmethod
    @abstractmethod
    def validate_inputs():
        """
         Abstract method to validate inputs.

         This method must be implemented by any subclass to define specific
         validation logic for the inputs.
         """
