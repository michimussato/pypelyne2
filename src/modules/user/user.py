class User(object):
    def __init__(self, d):
        super(User, self).__init__()
        self.__dict__ = d

    @property
    def project_roles(self):
        return self.__dict__[u'project_roles']

    @property
    def department_roles(self):
        return self.__dict__[u'department_roles']

    @property
    def password_decrypt(self):
        pass

    @property
    def id(self):
        return self.__dict__[u'id']

    @property
    def name_login(self):
        return self.__dict__[u'name_login']

    @property
    def name_full(self):
        return self.__dict__[u'name_full']
