import json
import logging
# import operator
import os
import pypelyne2.src.core.entities.entityproject as entityproject
import pypelyne2.src.core.entities.entitycontainer as entitycontainer
import pypelyne2.src.core.entities.entitytask as entitytask
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_entities():

    """Parses the pypelyne2.src.conf.settings.taskS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of task dicts.

    """

    logging.info('parsing entities')

    entities_list = []

    for database_file in SETTINGS.DATABASE_FILES:

        logging.info('processing entity source file: [P_DATABASE]{0}{1}'.format(os.sep, database_file))

        with open(os.path.join(SETTINGS.DATABASE_DIR, database_file), 'r') as f:
            entity_object = json.load(f)

            entities_list.append(entity_object)

            # if container_identifier is None:
            #     tasks_list.append(task_object)
            # else:
            #     if container_identifier == task_object['parent']:
            #         tasks_list.append(task_object)

    # for project_file in SETTINGS.PROJECTS_FILES:
    #
    #     logging.info('processing project source file: {0}'.format(project_file))
    #     with open(os.path.join(SETTINGS.PROJECTS_DIR, project_file), 'r') as f:
    #         project_object = json.load(f)
    #
    #         tasks_list.append(project_object)

        # plugin_dict = {}
    # for task in tasks:
    #     task['entity_type'] = 'task'

    # for task in tasks:
    #     if task[u'task_icon'] is not None:
    #         try:
    #             task[u'task_icon'] = os.path.join(SETTINGS.taskS_ICONS, task[u'task_icon'])
    #         except Exception, e:
    #             logging.error(e)
    #             task[u'task_icon'] = None

    # return sorted(tasks_list)
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

    for entity in entities:

        new_entity_object = None

        if entity[u'entity_type'] == 'project':
            new_entity_object = entityproject.EntityProject(d=entity,
                                                            entity_identifier=entity[u'identifier'])

        elif entity[u'entity_type'] == 'container':
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

        # elif entity['entity_type'] == 'task':
        #     pass

        entity_objects.add(new_entity_object)

    # for i in entity_objects:
    #     print i.identifier

    return entity_objects
