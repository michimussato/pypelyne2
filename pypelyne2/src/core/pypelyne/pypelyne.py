import logging
import uuid
import pypelyne2.src.core.entities.entity as entity
import pypelyne2.src.core.entities.entitycontainer as entitycontainer
import pypelyne2.src.core.entities.entityproject as entityproject
import pypelyne2.src.core.entities.entitytask as entitytask
import pypelyne2.src.core.entities.entityoutput as entityoutput
import pypelyne2.src.core.parser.projects.parse_projects as parse_projects
import pypelyne2.src.core.parser.entities.parse_entities as parse_entities
import pypelyne2.src.core.parser.resources.rcontainer.parse_rcontainers as parse_rcontainers
import pypelyne2.src.core.parser.resources.routput.parse_routputs as parse_routputs
import pypelyne2.src.core.parser.resources.rplugin.parse_rplugins as parse_rplugins
import pypelyne2.src.core.parser.resources.rtask.parse_rtasks as parse_rtasks


# class Pypelyne(pypelyne_abc.Pypelyne):
class Pypelyne(object):
    def __init__(self):
        super(Pypelyne, self).__init__()

        self._rplugins = None
        self._rcontainers = None
        self._rtasks = None
        self._routputs = None
        self._projects = None
        self._entities = None

    @property
    def rplugins(self):

        if self._rplugins is None:

            self._rplugins = parse_rplugins.get_rplugins()

        return self._rplugins

    @property
    def rcontainers(self):

        if self._rcontainers is None:
            self._rcontainers = parse_rcontainers.get_rcontainers()

        return self._rcontainers

    @property
    def rtasks(self):

        if self._rtasks is None:
            self._rtasks = parse_rtasks.get_rtasks()

        return self._rtasks

    @property
    def routputs(self):

        if self._routputs is None:
            self._routputs = parse_routputs.get_routputs()

        return self._routputs

    @property
    def projects(self):

        if self._projects is None:
            self._projects = parse_projects.get_projects()

        return self._projects

    @property
    def entities(self):

        if self._entities is None:
            self._entities = parse_entities.get_entities(rplugins=self.rplugins,
                                                         rcontainers=self.rcontainers,
                                                         rtasks=self.rtasks,
                                                         routputs=self.routputs)

        return self._entities

    def reload_resources(self):

        """If we need to reparse the resources, we can simply set
        everything in here to None so that the properties will
        do a fresh parse. we don't want this behaviour upon every
        single call of those properties. only on request."""

        self._rplugins = None
        self._rcontainers = None
        self._rtasks = None
        self._routputs = None

    def reload_entities(self):

        self._entities = None

    def reload_projects(self):

        self._projects = None

    def reload_all(self):

        self.reload_projects()
        self.reload_entities()
        self.reload_resources()

    def reload(self):

        self.reload_all()

    def get_projects(self):

        return self.projects

    def objectify_uuid(self, identifier):

        """takes an uuid identifer
            :returns: the Entity with that identifier"""

        objectified = None

        for item in self.projects | self.entities:

            if str(item.identifier) == str(identifier):
                objectified = item

                continue

        return objectified

    def set_project_object(self, entity_item):

        """the entities come with an attribute project_identifier which is a uuid string.
        depending on this we want to assign a EntityProject object directly using
        the new attribute project_object if it does not exist on the entity_item yet"""

        if 'project_object' not in entity_item.__dict__:

            for project_item in self.projects:

                if str(project_item.identifier) == str(entity_item.project_identifier):

                    setattr(entity_item, 'project_object', project_item)

                    return

    def get_entities(self, projects=None, entity_types=['container',
                                                        'task',
                                                        'output',
                                                        'version',
                                                        'publish',
                                                        'live']):

        """takes an optional list of project uuid identifers or EntityProject entities or a combination
        if an identifier is supplied, we get its corresponding object first with objectify_uuid
        also takes a list of entity type filters. shortcut for all is ['all']
            :returns: a list of dicts in the format of
            [{project: EntityProject, entities: set([Entity, Entity, Entity])},
             {project: EntityProject, entities: set([Entity, Entity, Entity])}]"""

        projects_list = list()

        projects = projects or self.projects

        for project_item in list(projects):

            entities_dict = dict()
            project_entities = set()

            for entity_item in self.entities:

                self.set_project_object(entity_item=entity_item)

                if not isinstance(project_item, entityproject.EntityProject):

                    """if project_item is not an EntityProject but an uuid string
                    assign the project object that relates to this uuid"""

                    project_item = self.objectify_uuid(str(project_item))

                if entity_item.project_object == project_item:

                    if 'all' in entity_types or 'container' in entity_types:

                        if isinstance(entity_item, entitycontainer.EntityContainer):
                            project_entities.add(entity_item)

                    if 'all' in entity_types or 'task' in entity_types:

                        if isinstance(entity_item, entitytask.EntityTask):
                            project_entities.add(entity_item)

                    if 'all' in entity_types or 'output' in entity_types:

                        pass

                    if 'all' in entity_types or 'version' in entity_types:

                        pass

                    if 'all' in entity_types or 'publish' in entity_types:

                        pass

                    if 'all' in entity_types or 'live' in entity_types:

                        pass

                entities_dict['project'] = project_item
                entities_dict['entities'] = project_entities

            projects_list.append(entities_dict.copy())

        return projects_list

    def get_containers(self, projects=None):

        """takes an optional list of project identifers or a project objects or a combination
        :returns: a set container entities"""

        containers = set()

        for entity_item in self.get_entities(projects):

            if isinstance(entity_item, entitycontainer.EntityContainer):

                containers.add(entity_item)

        return containers

    def get_tasks(self, projects=None):

        """takes an optional list of project identifers or a project objects or a combination
            :returns: a set of task entities"""

        tasks = set()

        for entity_item in self.get_entities(projects):

            if isinstance(entity_item, entitytask.EntityTask):
                tasks.add(entity_item)

        return tasks

    def get_outputs(self, projects=None):

        """takes an optional list of project identifers or a project objects or a combination
            :returns: a set of output entities"""

        outputs = set()

        for entity_item in self.get_entities(projects):

            if isinstance(entity_item, entityoutput.EntityOutput):
                outputs.add(entity_item)

        return outputs
