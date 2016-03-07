# import unittest
# import random
import pypelyne2.src.modules.core.parser.parse_plugins as parse_plugins


# class PluginTester(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#
#         cls.plugins = parse_plugins.get_plugins()
#
#     def setUp(self):
#
#         self.attributes = dir(self.plugins[0])
#
#     def test_plugin(self):
#
#         for attribute in self.attributes:
#             print '%s = %s' % (attribute, getattr(self.plugins[1], attribute))

plugins = parse_plugins.get_plugins()

# print dir(plugin)
for plugin in plugins:
    print
    print
    print 'processing {0}'.format(plugin)
    print dir(plugin)
    for attribute in dir(plugin):
        print '%s = %s' % (attribute, getattr(plugin, attribute))
