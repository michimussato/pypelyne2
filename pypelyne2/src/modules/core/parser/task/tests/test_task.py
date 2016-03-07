import unittest

import pypelyne2.src.modules.core.parser.parse_tasks as parse_tasks


class TaskTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.tasks = parse_tasks.get_tasks()

    def setUp(self):

        self.attributes = dir(self.tasks[0])

    def test_task(self):

        for attribute in self.attributes:
            print '%s = %s' % (attribute, getattr(self.tasks[1], attribute))
