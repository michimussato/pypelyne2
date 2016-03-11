import logging
import operator
import random

import PyQt4.QtCore as QtCore
import pypelyne2.src.core.parser.resources.plugin.parse_plugins as parse_plugins
import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.parser.parse_outputs as parse_outputs

import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.connection.connection as connection
import pypelyne2.src.modules.ui.containerui.containerui as containerui
import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.ui.portwidget.portwidget as portwidget


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

        self.main_scene = None

        self.containers = []
        self.container_connections = []

        self.nodes = []
        self.node_connections = []

    def set_main_scene(self, scene):

        """Sets the main_scene to scene. Used to refresh all container labels."""

        self.main_scene = scene

    def create_container(self, scene, container_object='random', position=QtCore.QPoint(0, 0)):

        """Creates a new container in main_scene scene"""

        logging.info('puppeteer.create_container() ({0})'.format(scene))

        if container_object == 'random':
            container_object = parse_containers.get_containers()[random.randint(0, len(
                parse_containers.get_containers()) - 1)]

        container_item = containerui.ContainerUI(puppeteer=self,
                                                 position=position,
                                                 container_object=container_object,
                                                 main_scene=scene)
        container_item.setScale(scene.global_scale)
        scene.addItem(container_item)
        scene.node_items.append(container_item)
        scene.addItem(container_item)

        return container_item

    def delete_container(self, container):
        logging.info('puppeteer.delete_container() ({0})'.format(None))

        container.scene_object.removeItem(container)

    def create_node(self,
                    scene,
                    plugin_object='random',
                    position=QtCore.QPoint(0, 0)):

        """Creates a new node in container_scene scene"""

        logging.info('puppeteer.create_node() ({0})'.format(scene))

        if plugin_object == 'random':

            plugin_object = parse_plugins.get_plugins()[random.randint(0, len(parse_plugins.get_plugins()) - 1)].x32

        node_item = nodeui.NodeUI(puppeteer=self,
                                  position=position,
                                  plugin=plugin_object,
                                  scene_object=scene)

        if SETTINGS.NODE_CREATE_COLLAPSED:
            node_item.expand_layout()
        node_item.setScale(scene.global_scale)
        scene.addItem(node_item)
        node_item.setParentItem(scene.base_rect)
        scene.node_items.append(node_item)

        scene.container_object.update_label()

        return node_item

    def create_output(self, node, output_object='random'):

        """Adds a new output to node"""

        if output_object == 'random':
            output_object = parse_outputs.get_outputs()[random.randint(0, len(parse_outputs.get_outputs()) - 1)]

        output = portwidget.Output(puppeteer=self,
                                   output_object=output_object,
                                   node_object=node,
                                   port_id=None)

        node.outputs.append(output)

        node.outputs = sorted(node.outputs,
                              key=operator.attrgetter(SETTINGS.SORT_NODE_PORTS_PRIMARY),
                              reverse=SETTINGS.SORT_NODE_PORTS_REVERSE)

        output.setParentItem(node)
        node.resize()

        return output

    def create_input(self, node, scene, output_object=None, start_port_id=None):

        """Adds a new input to a node.
        node-->node. no automatic connection creation"""

        start_item = self.find_output_graphics_item(scene=scene,
                                                    port_id=start_port_id)

        if start_item.node_object == node:
            logging.info('dont connect to itself')
            return 0

        for input_item in node.inputs:
            if start_item.object_id == input_item.object_id:
                logging.info('nodes are already connected')
                return 0

        input_item = portwidget.Input(puppeteer=self,
                                      output_object=output_object,
                                      port_id=start_port_id,
                                      start_item=start_item,
                                      node_object=node)

        node.inputs.append(input_item)
        input_item.setParentItem(node)

        node.inputs = sorted(node.inputs,
                             key=operator.attrgetter(SETTINGS.SORT_NODE_PORTS_PRIMARY),
                             reverse=SETTINGS.SORT_NODE_PORTS_REVERSE)

        node.resize()

        return input_item

    def create_asset_output(self, node, scene, container_object, output_object=None, start_port_id=None):

        """Adds an output port to a container.
        node-->assetOut. No automatic connection creation."""

        input_item = self.create_input(node=node,
                                       scene=scene,
                                       output_object=output_object,
                                       start_port_id=start_port_id)

        if input_item == 0:

            logging.info('output is already part of the container output')

        else:

            # container_object.output_port.outputs.append(output_object)
            container_object.output_port.outputs.add(output_object)

            self.update_container_labels()

        return input_item

    # def create_asset_input(self, container, start_port_id):
    #
    #     for container_item in self.main_scene.node_items:
    #
    #         start_item = self.find_output_graphics_item(scene=container_item.container_scene,
    #                                                     port_id=start_port_id)
    #
    #         if start_item != 0:
    #             container_temp = container_item
    #             logging.info('source port object found')
    #             break
    #
    #     print start_item
    #
    #     new_input = portwidget.AssetInput(puppeteer=self,
    #                                       container=container_temp,
    #                                       node_object=container.container_scene.input_area,
    #                                       output_object=start_item.output_object,
    #                                       port_id=start_item.object_id,
    #                                       start_item=start_item)
    #
    #     # new_input = portwidget.Output(puppeteer=self,
    #     #                               node_object=start_item.node_object,
    #     #                               output_object=start_item.output_object,
    #     #                               port_id=start_item.object_id)
    #
    #     container.container_scene.input_area.add_output(port=new_input)
    #
    #     # return new_input

    def add_input_container(self, scene, port_id=None, end_item=None):

        """Adds an input and a connection for
        container-->container"""

        start_item = self.find_output_graphics_item(scene=scene, port_id=port_id)

        if start_item.container == end_item.container:
            logging.info('dont connect to itself')
            return 0

        if start_item.container in end_item.container.upstream_containers:
            logging.info('containers are already connected')
            return 0

        # end_item.container.upstream_containers.append(start_item.container)
        end_item.container.upstream_containers.add(start_item.container)

        self.update_container_labels()

        return end_item

    def update_container_labels(self):

        """Refreshes all container labels"""

        for container in self.main_scene.node_items:
            container.update_label()

        # self.update_container_input_source_area()

    # def update_container_input_source_area(self):
    #     for container in self.main_scene.node_items:
    #         container.update_inputs_source_area()

    def add_connection_container(self, scene, start_port_id, end_item):

        """Adds a container-->container connection"""

        start_item = self.find_output_graphics_item(scene=scene,
                                                    port_id=start_port_id)

        connection_line = connection.Connection(start_item=start_item,
                                                end_item=end_item,
                                                scene_object=scene)

        scene.addItem(connection_line)

        return connection_line

    def add_connection(self, start_port_id, end_item, scene):

        """Adds a node-->node connection"""

        start_item = self.find_output_graphics_item(scene=scene,
                                                    port_id=start_port_id)

        connection_line = connection.Connection(start_item=start_item,
                                                end_item=end_item,
                                                scene_object=scene)

        start_item.downstream_connections.append(connection_line)
        start_item.downstream_ports.append(end_item)
        end_item.upstream_connections.append(connection_line)

        return connection_line

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

        """Finds an QGraphicsItem in a scene by object_id"""

        logging.info('looking for port with id {0}'.format(port_id))
        # does it make sense to do this scene dependent?
        for node_item in scene.node_items:
            for output_graphics_item in node_item.outputs:
                if output_graphics_item.object_id == port_id:
                    logging.info('output_graphics_item of port_id {0} found: {1}'.format(port_id, output_graphics_item))
                    return output_graphics_item
            logging.warning('output_graphics_item of port_id {0} not found'.format(port_id))
            return 0
