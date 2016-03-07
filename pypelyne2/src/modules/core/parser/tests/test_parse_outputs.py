import unittest

import pypelyne2.src.parser.parse_outputs as parse_outputs

import pypelyne2.src.modules.core.parser.output.output as output


class ParseOutputsTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.output_objects = parse_outputs.get_outputs()

    def test_get_outputs(self):
        """ Test checks if the outputs are output objects """
        for output_object in self.output_objects:
            self.assertIsInstance(output_object, output.Output)

    def test_abbreviation(self):
        """ Test checks if the output object has this method """
        self.assertTrue('abbreviation' in dir(self.output_objects[0]))

    def test_color(self):
        """ Test checks if the output object has this method """
        self.assertTrue('color' in dir(self.output_objects[0]))

    def test_formats(self):
        """ Test checks if the output object has this method """
        self.assertTrue('_formats' in dir(self.output_objects[0]))

    def test_icon(self):
        """ Test checks if the output object has this method """
        self.assertTrue('icon' in dir(self.output_objects[0]))

    def test_output(self):
        """ Test checks if the output object has this method """
        self.assertTrue('output' in dir(self.output_objects[0]))

    def test_output_enable(self):
        """ Test checks if the output object has this method """
        self.assertTrue('output_enable' in dir(self.output_objects[0]))
