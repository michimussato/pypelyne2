class User(object):

    """Documentation for class Task(object)."""

    def __init__(self, d):

        """__init__.

        Args:
            d (dict): dictionary with the attributes for self
        """

        super(User, self).__init__()
        self.__dict__ = d

    @property
    def project_roles(self):

        """project_roles.

        Returns
        -------
        list
            (property) Returns a list the project_roles of self.
            One dict is in the form of:
            {
                u'project': u'project_1',
                u'roles':
                [
                    {
                        u'department': u'animation',
                        u'reports_to_users': [should be uuids],
                        u'role': u'artist'
                    },
                    {
                        u'department': u'fx',
                        u'reports_to_users': [should be uuids],
                        u'role': u'trainee'
                    }
                ]
            }
        """

        return self.__dict__[u'project_roles']

    @property
    def department_roles(self):

        """department_roles.

        Note
        ----
        Duplicated by department_reports_to?

        Returns
        -------
        list
            (property) Returns a list of dicts of department_roles of self.
            One dict is in the form of:
            {
                u'department': u'rnd',
                u'role': u'junior',
                u'reports_to_users':
                [
                    u'e2895852-8909-4fa9-b6bd-910698a7db77',
                    u'1b61f2a0-e2e2-4809-8eed-b7ef8e3966fb'
                ],
            }
        """

        return self.__dict__[u'department_roles']

    @property
    def password_decrypt(self):

        """password_decrypt.

        Returns
        -------
        str
            (property) Returns the decrypted password of self in the form of:
            <no yet implemented>
        """

        pass

    @property
    def id(self):

        """id.

        Returns
        -------
        str
            (property) Returns the uuid of self in the form of:
            1b61f2a0-e2e2-4809-8eed-b7ef8e3966fb
        """

        return self.__dict__[u'id']

    @property
    def name_login(self):

        """name_login.

        Returns
        -------
        str
            (property) Returns the unix like name of self in the form of:
            michaelmussato
        """

        return self.__dict__[u'name_login']

    @property
    def name_full(self):

        """name_full.

        Returns
        -------
        str
            (property) Returns the human name of self in the form of:
            Michael Mussato
        """

        return self.__dict__[u'name_full']

    @property
    def department_reports_to(self):

        """department_reports_to.

        Note
        ----
        Duplicate of department_roles? Maybe I had something specific in mind but
        couldn't get to the actual goal... Or department_roles already did the trick.
        Don't remember.

        Returns
        -------
        list
            (property) Returns a list of dicts self reports to depending on the department.
            A dict is in the form of:
            {
                u'department': u'rnd',
                u'role': u'junior',
                u'reports_to_users':
                [
                    u'e2895852-8909-4fa9-b6bd-910698a7db77',
                    u'1b61f2a0-e2e2-4809-8eed-b7ef8e3966fb'
                ],
            }
        """

        department_reports_to_list = []
        for department in self.department_roles:
            department_reports_to_list.append(department)

        return department_reports_to_list
