import unittest
# from unittest import TestResult
import os
import json
import src.modules.plugin

class TestPlugin(unittest.TestCase):
    def setUp(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))
        print self.dir
        self.src_dir = os.path.dirname(self.dir)
        self.plugins = [x
                        for x in os.listdir(os.path.join(self.src_dir, 'conf', 'plugins'))
                        if not x.startswith('_') and not os.path.isdir(x)]

    def test_plugin_objects(self):
        print self.plugins