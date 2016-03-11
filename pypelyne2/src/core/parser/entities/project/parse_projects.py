import json
import logging
import operator
import os

import pypelyne2.src.core.entities.project as class_project

import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# import pypelyne2.src.modules.container.container as class_container
# import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_projects():

    """Parses the pypelyne2.src.conf.settings.CONTAINERS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of container dicts.

    """

    logging.info('parsing projects')

    projects_list = []

    for project_file in SETTINGS.PROJECTS_FILES:

        logging.info('processing project source file: {0}'.format(project_file))
        with open(os.path.join(SETTINGS.PROJECTS_DIR, project_file), 'r') as f:
            project_object = json.load(f)

            projects_list.append(project_object)

        # plugin_dict = {}
    # for container in containers:
    #     container['entity_type'] = 'container'

    # for container in containers:
    #     if container[u'container_icon'] is not None:
    #         try:
    #             container[u'container_icon'] = os.path.join(SETTINGS.CONTAINERS_ICONS, container[u'container_icon'])
    #         except Exception, e:
    #             logging.error(e)
    #             container[u'container_icon'] = None

    return sorted(projects_list,
                  key=operator.itemgetter(SETTINGS.SORT_PROJECTS),
                  reverse=SETTINGS.SORT_PROJECTS_REVERSE)


def get_projects():

    """Get all Container() objects in a list

    :returns: list -- of pypelyne2.src.modules.container.container.Container() objects

    """

    project_objects = []
    projects = parse_projects()
    for project in projects:
        new_container_object = class_project.Project(project)
        project_objects.append(new_container_object)

    return project_objects
