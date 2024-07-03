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
        pass
