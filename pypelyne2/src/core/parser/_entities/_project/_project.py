class Project(object):
    def __init__(self, d):
        super(Project, self).__init__(d)

        self.__dict__ = d
