import random
import PyQt4.QtCore as QtCore
import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.parser.parse_plugins as parse_plugins
import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.ui.containerui.containerui as containerui
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


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
        super(Puppeteer, self).__init__()

        # self.global_scale = 1

        self.containers = []
        self.container_connections = []

        self.nodes = []
        self.node_connections = []

    def create_container(self, scene, container=None, position=QtCore.QPoint(0, 0)):

        container_object = container or parse_containers.get_containers()[random.randint(0, len(parse_containers.get_containers())-1)]

        container_item = containerui.ContainerUI(puppeteer=self, position=position, container=container_object, scene_object=scene)
        container_item.setScale(scene.global_scale)
        scene.addItem(container_item)
        scene.node_items.append(container_item)
        scene.addItem(container_item)

        return container_item

    def create_node(self, scene, plugin=None, position=QtCore.QPoint(0, 0)):

        plugin = plugin or parse_plugins.get_plugins()[random.randint(0, len(parse_plugins.get_plugins())-1)].x32

        node_item = nodeui.NodeUI(puppeteer=self, position=position, plugin=plugin, scene_object=scene)
        if SETTINGS.NODE_CREATE_COLLAPSED:
            node_item.expand_layout()
        node_item.setScale(scene.global_scale)
        scene.addItem(node_item)
        node_item.setParentItem(scene.base_rect)
        scene.node_items.append(node_item)

        scene.container_object.update_label()

        return node_item

    @staticmethod
    def find_output_graphics_item(scene, port_id):
        # does it make sense to do this scene dependent?
        for node_item in scene.node_items:
            for output_graphics_item in node_item.outputs:
                if output_graphics_item.object_id == port_id:
                    return output_graphics_item
                else:
                    return None
