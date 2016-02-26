import unittest
import random
import pypelyne2.src.parser.parse_outputs as parse_outputs


class OutputTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.outputs = parse_outputs.get_outputs()

    # def setUp(self):
    #
    #     self.attributes = dir(self.output)

    def test_outputs(self):
        for output in self.outputs:
            print
            print
            print 'processing {0}'.format(output)
            print dir(output)
            for attribute in dir(output):
                print '%s = %s' % (attribute, getattr(output, attribute))

    # def test_all_outputs(self):
    #     print i.icon
