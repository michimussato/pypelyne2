# import unittest
# from unittest import TestResult
# import os
# import json
import src.parser.parse_plugins as parse_plugins
# import src.modules.plugin as plugin

plugins = parse_plugins.get_plugins()

# print plugins

print dir(plugins[0])

for plugin in plugins:
    print plugin.family, plugin.release_number, plugin.executable_x64, plugin.family_enable
