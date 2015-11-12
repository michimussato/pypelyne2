class Node(object):
    def __init__(self):
        super(Node, self).__init__()
        # self.container = False
        self.children = []  # nodes living inside as children
        self.siblings = []
        self.parents = []  # this node living in what nodes
        self.outputs = []
        self.inputs = []
        self.task = None
        self.tool = None
        self.id = None
        self.name = None
        # self.icon = None
        self.dependenies_req = None
        self.dependenies_opt = None
        self.creator = None
        self.modificators = None