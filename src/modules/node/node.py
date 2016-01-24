import uuid


class Node(object):
    def __init__(self, id=None):
        super(Node, self).__init__()
        # self.container = False
        self.children = []  # nodes living inside as children
        self.siblings = []
        self.parents = []  # this node living in what nodes
        self.outputs = []
        self.inputs = []
        self.task = None
        self.tool = None
        self.uuid = id or str(uuid.uuid4())
        self.name = None
        # self.icon = None
        self.dependenies_req = None
        self.dependenies_opt = None
        self.creator = None
        self.modificators = None
