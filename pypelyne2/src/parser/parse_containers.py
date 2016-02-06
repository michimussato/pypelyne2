import json
import logging
import operator
import pypelyne2.src.modules.container.container as class_container
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_containers():
    logging.info('parsing containers')

    with open(SETTINGS.CONTAINERS_FILE, 'r') as f:
        json_object = json.load(f)

    containers = [container for container in json_object if container['container_enable']]

    # for container in containers:
    #     container['entity_type'] = 'container'

    return sorted(containers,
                  key=operator.itemgetter(SETTINGS.SORT_CONTAINERS),
                  reverse=SETTINGS.SORT_CONTAINERS_REVERSE)


def get_containers():
    container_objects = []
    containers = parse_containers()
    for container in containers:
        new_container_object = class_container.Container(container)
        container_objects.append(new_container_object)

    return container_objects
