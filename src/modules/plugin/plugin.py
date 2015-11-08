class PlugIn(object):
    def __init__(self, d):
        super(PlugIn, self).__init__()
        self.__dict__ = d
        # self.dict_x32 = None
        # self.dict_x64 = None

    def create_project(self, location=None):
        pass

    def launch_instance(self, location=None):
        self.create_project(location=location)
        pass

    def launch_task(self, node=None):
        pass
