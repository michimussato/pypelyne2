class Puppeteer(object):

    """This is the Puppeteer.
    It is supposed to take care of thinks like:
    - self.find_item_by_uuid(uuid)
    - self.create_container(uuid=None)
    - self.remove_container(uuid)
    - self.create_node(uuid=None)
    - self.remove_node(uuid)
    - self.create_output(uuid=None)
    - self.remove_output(uuid)
    - self.create_connection(uuid=None, uuid_src, uuid_dst)
    - self.remove_connection(uuid)
    - self.get_node_of_output(uuid_output)
    - self.get_container_of_node(uuid_node)
    - self.nodes = []
    - self.get_scene(uuid_node or uuid_container or uuid_output)
    - self.containers = []
    - self.connections = []
    - self.return_items_of_type(type=node/container/connection/output)
    - self.return_upstream_node(uuid_input)
    - self.return_downstream_nodes(uuid_output or uuid_node)
    - sefl.return_downstream_containers()


    """
    def __init__(self):
        super(Manager, self).__init__()

