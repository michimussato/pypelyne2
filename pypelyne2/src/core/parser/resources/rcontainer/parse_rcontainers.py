import json
import logging
import operator
import os

import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.core.resources.rcontainer as rcontainer


def parse_rcontainers():

    """Parses the pypelyne2.src.conf.settings.CONTAINERS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of container dicts.
    
    """

    logging.info('parsing containers')

    with open(SETTINGS.CONTAINERS_FILE, 'r') as f:
        json_object = json.load(f)

    containers = [container for container in json_object if container[u'container_enable']]

    # for container in containers:
    #     container['entity_type'] = 'container'

    for container in containers:
        if container[u'container_icon'] is not None:
            try:
                container[u'container_icon'] = os.path.join(SETTINGS.CONTAINERS_ICONS, container[u'container_icon'])
            except Exception, e:
                logging.error(e)
                container[u'container_icon'] = None

    return sorted(containers,
                  key=operator.itemgetter(SETTINGS.SORT_CONTAINERS),
                  reverse=SETTINGS.SORT_CONTAINERS_REVERSE)


def get_rcontainers():

    """Get all Container() objects in a list

    :returns: list -- of pypelyne2.src.modules.container.container.Container() objects

    """

    container_objects = set()
    containers = parse_rcontainers()
    for container in containers:
        new_container_object = rcontainer.RContainer(container)
        container_objects.add(new_container_object)

    return container_objects
