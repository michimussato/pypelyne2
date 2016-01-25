import unittest
import pypelyne2.src.parser.parse_users as parse_users


class UserTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.users = parse_users.get_users()

    def setUp(self):

        self.attributes = dir(self.users[0])

    def test_user(self):

        for attribute in self.attributes:
            print '%s = %s' % (attribute, getattr(self.users[0], attribute))

    def test_properties(self):
        print self.users[0].id
        print self.users[0].project_roles
        print self.users[0].department_roles
        print self.users[0].name_login
