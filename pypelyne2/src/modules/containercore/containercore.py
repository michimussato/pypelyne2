import uuid
# import logging


class ContainerCore(object):
    def __init__(self, container_type=None, container_id=None, name_string=None):
        super(ContainerCore, self).__init__()

        self.uuid = container_id or str(uuid.uuid4())

        # self.container = container or parse_containers.get_containers()[random.randint(0, len(parse_containers.get_containers())-1)]

        self.name_string = name_string or self.uuid

        # all the nodes contained in self
        self.child_items = []

        # asset, shot, sequence, prop, character etc
        self.container_type = container_type
        self.outputs = []
        self.inputs = []
