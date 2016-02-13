import logging
import random
import PyQt4.QtCore as QtCore
import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.parser.parse_plugins as parse_plugins
import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.ui.containerui.containerui as containerui
import pypelyne2.src.modules.ui.connection.connection as connection
import pypelyne2.src.modules.ui.portwidget.portwidget as output
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
        logging.info('puppeteer.create_container() ({0})'.format(scene))

        container_object = container or parse_containers.get_containers()[random.randint(0, len(parse_containers.get_containers())-1)]

        container_item = containerui.ContainerUI(puppeteer=self, position=position, container=container_object, scene_object=scene)
        container_item.setScale(scene.global_scale)
        scene.addItem(container_item)
        scene.node_items.append(container_item)
        scene.addItem(container_item)

        return container_item

    def delete_container(self, container):
        logging.info('puppeteer.delete_container() ({0})'.format(None))

        container.scene_object.removeItem(container)

        # pass

    def create_node(self, scene, plugin=None, position=QtCore.QPoint(0, 0)):
        logging.info('puppeteer.create_node() ({0})'.format(scene))

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

    def add_input(self, scene, node, output_object=None, port_id=None, create_connection=True):

        start_item = self.find_output_graphics_item(scene=scene, port_id=port_id)

        end_item = output.Input(node_object=scene,
                                output_object=output_object,
                                port_id=port_id,
                                start_item=start_item)

        node.inputs.append(end_item)
        end_item.setParentItem(node)

        if create_connection:
            self.add_connection(scene=scene, node=node, start_item=start_item, end_item=end_item)

        node.resize()

    def add_input_container(self, scene, port_id=None, end_item=None):

        start_item = self.find_output_graphics_item(scene=scene, port_id=port_id)
        self.add_connection_container(scene=scene, start_item=start_item, end_item=end_item)

    @staticmethod
    def add_connection_container(scene, start_item, end_item):

        connection_line = connection.Connection(start_item=start_item,
                                                end_item=end_item,
                                                scene_object=scene)

        scene.addItem(connection_line)

    @staticmethod
    def add_connection(scene, node, start_item, end_item):
        connection_line = connection.Connection(start_item=start_item,
                                                end_item=end_item,
                                                scene_object=scene)

        node.connections.append(connection_line)
        scene.addItem(connection_line)
        scene.connection_items.append(connection_line)

        start_item.downstream_connections.append(connection_line)
        start_item.downstream_ports.append(end_item)
        end_item.upstream_connections.append(connection_line)

    @staticmethod
    def delete_node(node):
        logging.info('puppeteer.delete_node() ({0})'.format(node))

        temp_list_copy_inputs = list(node.inputs)
        temp_list_copy_outputs = list(node.outputs)

        for input_item in temp_list_copy_inputs:
            input_item.remove_input()

        for output_item in temp_list_copy_outputs:
            output_item.remove_output()

        del temp_list_copy_inputs
        del temp_list_copy_outputs

        node.scene_object.node_items.remove(node)

        node.scene_object.removeItem(node)

        print 'items left in scene:'
        for i in node.scene_object.items():
            print type(i)

    @staticmethod
    def find_output_graphics_item(scene, port_id):
        logging.info('looking for port with id {0}'.format(port_id))
        # does it make sense to do this scene dependent?
        for node_item in scene.node_items:
            for output_graphics_item in node_item.outputs:
                if output_graphics_item.object_id == port_id:
                    logging.info('output_graphics_item of port_id {0} found: {1}'.format(port_id, output_graphics_item))
                    # print 'output_graphics_item of port_id {0} found: {1}'.format(port_id, output_graphics_item)
                    return output_graphics_item
            logging.warning('output_graphics_item of port_id {0} not found'.format(port_id))
            # print 'output_graphics_item of port_id {0} not found'.format(port_id)
