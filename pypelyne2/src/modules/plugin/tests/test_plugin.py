import unittest
import pypelyne2.src.parser.parse_plugins as parse_plugins


class PluginTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.plugins = parse_plugins.get_plugins()

    def setUp(self):

        self.attributes = dir(self.plugins[0])

    def test_plugin(self):

        for attribute in self.attributes:
            print '%s = %s' % (attribute, getattr(self.plugins[1], attribute))
