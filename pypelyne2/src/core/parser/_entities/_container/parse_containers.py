import json
import logging
import operator
import os
# import pypelyne2.src.core.entities.entityproject as entityproject
import pypelyne2.src.core.entities.entitycontainer as entitycontainer
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# import pypelyne2.src.modules.container.container as class_container
# import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_containers(project_identifier):

    """Parses the pypelyne2.src.conf.settings.CONTAINERS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of container dicts.

    """

    logging.info('parsing containers')

    containers_list = []

    for database_file in SETTINGS.DATABASE_FILES:

        # print os.path.join(os.environ[u'P_DATABASE'], json_file)
        # logging.info('processing project source file: [P_PROJECTS]{0}{1}'.format(os.sep, project_file))
        logging.info('processing database source file: [P_DATABASE]{0}{1}'.format(os.sep, database_file))

        with open(os.path.join(SETTINGS.DATABASE_DIR, database_file), 'r') as f:
            container_object = json.load(f)

            if container_object['entity_type'] != 'container':
                continue

            if project_identifier is None:
                containers_list.append(container_object)

            else:
                if project_identifier == container_object['parent']:
                    containers_list.append(container_object)

    # for project_file in SETTINGS.PROJECTS_FILES:
    #
    #     logging.info('processing project source file: {0}'.format(project_file))
    #     with open(os.path.join(SETTINGS.PROJECTS_DIR, project_file), 'r') as f:
    #         project_object = json.load(f)
    #
    #         containers_list.append(project_object)

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

    # return sorted(containers_list)
    return containers_list


def get_containers(project_identifier=None):

    """Get all Container() objects in a list

    :returns: list -- of pypelyne2.src.modules.container.container.Container() objects

    """

    container_objects = []
    containers = parse_containers(project_identifier)
    for container in containers:
        # print project
        new_container_object = entitycontainer.EntityContainer(container)
        container_objects.append(new_container_object)

    return container_objects
