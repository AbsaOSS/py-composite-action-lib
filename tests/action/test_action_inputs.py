import unittest

from action.action_inputs import BaseActionInputs


class ConcreteActionInputs(BaseActionInputs):
    @staticmethod
    def validate_inputs():
        return True


def test_cannot_instantiate_base_class():
    with unittest.TestCase().assertRaises(TypeError):
        _ = BaseActionInputs()
