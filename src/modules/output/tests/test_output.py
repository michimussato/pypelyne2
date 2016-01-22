import unittest
import src.parser.parse_outputs as parse_outputs


class OutputTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.outputs = parse_outputs.get_outputs()

    def setUp(self):

        self.attributes = dir(self.outputs[0])

    def test_outputs(self):

        for attribute in self.attributes:
            print '%s = %s' % (attribute, getattr(self.outputs[1], attribute))
