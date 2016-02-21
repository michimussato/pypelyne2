import random
import pypelyne2.src.modules.uuidobject.uuidobject as uuidobject
import pypelyne2.src.modules.ui.graphicsscene.graphicsscenenodes as graphicsscenenodes
import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.modules.ui.containerdroparea.containerdroparea as containerdroparea


class ContainerCore(uuidobject.UuidObject):
    def __init__(self,
                 puppeteer,
                 container_type=None,
                 container_id=None,
                 name_string=None,
                 main_scene=None,
                 container_object=None):
        super(ContainerCore, self).__init__(object_type='container',
                                            object_id=container_id)

        self.puppeteer = puppeteer

        self.name_string = name_string or self.object_id

        self.main_scene = main_scene

        self.view_object = self.main_scene.view_object

        self.container_scene = graphicsscenenodes.GraphicsSceneNodes(puppeteer=self.puppeteer,
                                                                     view_object=self.view_object,
                                                                     container_object=self)

        self.container = container_object or parse_containers.get_containers()[random.randint(0, len(parse_containers.get_containers())-1)]

        self.drop_area = containerdroparea.ContainerDropArea(puppeteer=self.puppeteer,
                                                             container_core=self)

        # all the nodes contained in self
        self.child_nodes = []

        # all output objects of self
        self.container_output_channels = []

        # all input objects of self
        self.container_input_channels = []

        self.connections = []

        # asset, shot, sequence, prop, character etc
        self.container_type = container_type

        # self.upstream_containers = []
        self.upstream_containers = set()

        self.outputs = []
        self.inputs = []
        # self.inputs = set()
