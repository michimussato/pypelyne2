import pypelyne2.src.modules.uuidobject.uuidobject as uuidobject


class ContainerCore(uuidobject.UuidObject):
    def __init__(self, container_type=None, container_id=None, name_string=None):
        super(ContainerCore, self).__init__(object_type='container', object_id=container_id)

        self.name_string = name_string or self.object_id

        # all the nodes contained in self
        self.child_items = []

        self.connections = []

        # asset, shot, sequence, prop, character etc
        self.container_type = container_type
        self.outputs = []
        self.inputs = []
