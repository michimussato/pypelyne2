import json
import logging
# import operator
import os
# import pypelyne2.src.core.entities.entityproject as entityproject
import pypelyne2.src.core.entities.entitycontainer as entitycontainer
import pypelyne2.src.core.entities.entitytask as entitytask
import pypelyne2.src.core.entities.entityoutput as entityoutput
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_entities():

    """Parses the pypelyne2.src.conf.settings.taskS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of task dicts.

    """

    logging.info('parsing entities')

    entities_list = []

    for entity_file in SETTINGS.DATABASE_FILES_ENTITIES:

        logging.info('processing entity source file: [P_DATABASE_ENTITIES]{0}{1}'.format(os.sep, entity_file))

        # print SETTINGS.DATABASE_DIR_ENTITIES
        #
        # print database_file
        #
        # print os.path.join(SETTINGS.DATABASE_DIR_ENTITIES, database_file)

        with open(os.path.join(SETTINGS.DATABASE_DIR_ENTITIES, entity_file), 'r') as f:
            entity_object = json.load(f)

            entities_list.append(entity_object)

    return entities_list


def get_entities(**kwargs):

    """Get all task() objects in a list

    :returns: list -- of pypelyne2.src.modules.task.task.Task() objects

    """

    entity_objects = set()
    entities = parse_entities()

    # print kwargs[u'rcontainers']
    # print kwargs[u'rtasks']
    # print kwargs[u'rplugins']
    # print kwargs[u'routput']

    for entity in entities:

        new_entity_object = None

        # if entity[u'entity_type'] == 'project':
        #     new_entity_object = entityproject.EntityProject(d=entity,
        #                                                     entity_identifier=entity[u'identifier'])

        if entity[u'entity_type'] == 'container':
            rcontainer_object = None
            for rcontainer in kwargs[u'rcontainers']:
                if rcontainer.identifier == entity[u'entity_specific'][u'rcontainer']:
                    rcontainer_object = rcontainer
                    break
            new_entity_object = entitycontainer.EntityContainer(d=entity,
                                                                entity_identifier=entity[u'identifier'],
                                                                rcontainer=rcontainer_object)

        elif entity[u'entity_type'] == 'task':
            rtask_object = None
            for rtask in kwargs[u'rtasks']:
                if rtask.identifier == entity[u'entity_specific'][u'rtask']:
                    rtask_object = rtask
                    break
            rplugin_object = None
            for rplugin in kwargs[u'rplugins']:
                if rplugin.identifier == entity[u'entity_specific'][u'rplugin']:
                    rplugin_object = getattr(rplugin, entity[u'entity_specific'][u'rplugin_arch'])
                    break
            new_entity_object = entitytask.EntityTask(d=entity,
                                                      entity_identifier=entity[u'identifier'],
                                                      rtask=rtask_object,
                                                      rplugin=rplugin_object)

        elif entity[u'entity_type'] == 'output':
            routput_object = None
            for routput in kwargs[u'routputs']:
                if routput.identifier == entity[u'entity_specific'][u'routput']:
                    routput_object = routput
                    break
            new_entity_object = entityoutput.EntityOutput(d=entity,
                                                          entity_identifier=entity[u'identifier'],
                                                          routput=routput_object)

        entity_objects.add(new_entity_object)

    # for i in entity_objects:
    #     print i.identifier

    return entity_objects
