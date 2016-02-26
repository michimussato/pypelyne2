import pypelyne2.src.modules.core.entities.uuidobject as uuidobject


class NodeBase(uuidobject.UuidObject):
    def __init__(self):
        super(NodeBase, self).__init__()

        self. object_type = 'undefined'

        self.id = None

        self._inputs = set()
        self._outputs = set()


class NodeContainer(NodeBase):
    def __init__(self):
        super(NodeContainer, self).__init__()

        self. object_type = 'container'


class NodeTask(NodeBase):
    def __init__(self):
        super(NodeTask, self).__init__()

        self. object_type = 'task'
