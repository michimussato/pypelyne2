# import pypelyne2.src.modules.core.entities.entity as entity


class Pypelyne(object):
    def __init__(self):
        super(Pypelyne, self).__init__()

        self.project_entities = set()

        self.container_entities = set()
        self.task_entities = set()
        self.output_entities = set()

        self.entity_kwargs = set(['entity_uuid', 'entity_name', 'entity_object'])

        # overrides of base classes
        # self.entity_type = 'puppeteer'

    @property
    def loaded_entities(self):

        return self.container_entities | self.task_entities | self.output_entities

    def load_project(self):

        # self.container_entities.clear()
        # self.task_entities.clear()
        # self.output_entities.clear()

        pass

    def get_item(self, entity_uuid=None, entity_name=None, entity_object=None):

        if entity_uuid:

            entity_name = self.get_entity_name(entity_uuid)



        # elif entity_name:
        #
        #     entity_uuid = self.get_entity_uuid(entity_name)

        elif entity_object:

            pass

    def get_projects(self, project_status=None, project_client=None, project_name_pattern=None, project_type=None, project_fps=None, project_resolution=None, project_due_by=None):

        pass

    def project(self, **kwargs):

        entity_uuid=None, entity_name=None, entity_object=None

        # http://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/

        version = self.version(entity_uuid='0000-0000-00000000')
        output = self.output(entity_uuid='0000-0000-00000000')
        task = self.task(entity_uuid='0000-0000-00000000')
        container = self.container(entity_uuid='0000-0000-00000000')

        project = version.project()
        project = output.project()
        project = task.project()
        project = container.project()

        return False if argument or self is project

        return project of argument or of self

    def container(self, **kwargs):

        if len(kwargs) > 1:

            raise Exception, 'maximum one argument allowed'

            # return None  # max(len(kwargs)) is 1

        if kwargs is not None:

            if kwargs[0] not in self.entity_kwargs:

                raise Exception, 'unknown argument'

        if isinstance(self, VERSION):

            version = self.version(entity_uuid=kwargs['entity_uuid'])
            container = version.container()

        elif isinstance(self, OUTPUT):

            output = self.output(entity_uuid=kwargs['entity_name'])
            container = output.container()

        elif isinstance(self, TASK):

            task = self.task(entity_uuid=kwargs['entity_object'])
            container = task.container()

        else:

            raise Exception, 'object has no method "container()"'

        # return False if argument or self is project
        # return False if argument or self is container

        return container

    def task(self, entity_uuid=None, entity_name=None, entity_object=None):

        version = self.version(entity_uuid='0000-0000-00000000')
        output = self.output(entity_uuid='0000-0000-00000000')

        task = version.task()
        task = output.task()

        return False if argument or self is project
        return False if argument or self is container
        return False if argument or self is task

        return task of argument or of self

    def output(self, entity_uuid=None, entity_name=None, entity_object=None):

        version = self.version(entity_uuid='0000-0000-00000000')

        output = version.output()

        return False if argument or self is project
        return False if argument or self is container
        return False if argument or self is task
        return False if argument or self is output

        return output of argument or of self

    # def version(self, entity_uuid=None, entity_name=None, entity_object=None):
    #
    #     return version of argument or of self
