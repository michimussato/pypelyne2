import json
import logging
# import operator
import os
import pypelyne2.src.core.entities.entityproject as entityproject
# import pypelyne2.src.core.entities.entitycontainer as entitycontainer
# import pypelyne2.src.core.entities.entitytask as entitytask
# import pypelyne2.src.core.entities.entityoutput as entityoutput
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_projects():

    """Parses the pypelyne2.src.conf.settings.taskS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of task dicts.

    """

    logging.info('parsing projects')

    projects_list = []

    for project_file in SETTINGS.DATABASE_FILES_PROJECTS:

        logging.info('processing project source file: [P_DATABASE_PROJECTS]{0}{1}'.format(os.sep, project_file))

        with open(os.path.join(SETTINGS.DATABASE_DIR_PROJECTS, project_file), 'r') as f:
            project_object = json.load(f)
            projects_list.append(project_object)

    return projects_list


def get_projects():

    """Get all task() objects in a list

    :returns: list -- of pypelyne2.src.modules.task.task.Task() objects

    """

    project_objects = set()
    projects = parse_projects()

    # print kwargs[u'rcontainers']
    # print kwargs[u'rtasks']
    # print kwargs[u'rplugins']
    # print kwargs[u'routput']

    for project in projects:

        new_entity_object = None

        if project[u'entity_type'] == 'project':
            new_entity_object = entityproject.EntityProject(d=project,
                                                            entity_identifier=project[u'identifier'])

        project_objects.add(new_entity_object)

    return project_objects
