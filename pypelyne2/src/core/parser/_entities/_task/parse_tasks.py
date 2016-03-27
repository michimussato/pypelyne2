import json
import logging
import operator
import os
import pypelyne2.src.core.entities.entitytask as entitytask
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_tasks(container_identifier):

    """Parses the pypelyne2.src.conf.settings.taskS_FILE file and returns a sorted list of dicts.

    :returns: list -- a sorted list of task dicts.

    """

    logging.info('parsing tasks')

    tasks_list = []

    for database_file in SETTINGS.DATABASE_FILES:

        # print os.path.join(os.environ[u'P_DATABASE'], json_file)
        # logging.info('processing project source file: [P_PROJECTS]{0}{1}'.format(os.sep, project_file))
        logging.info('processing database source file: [P_DATABASE]{0}{1}'.format(os.sep, database_file))

        with open(os.path.join(SETTINGS.DATABASE_DIR, database_file), 'r') as f:
            task_object = json.load(f)

            if task_object['entity_type'] != 'task':
                continue

            if container_identifier is None:
                tasks_list.append(task_object)
            else:
                if container_identifier == task_object['parent']:
                    tasks_list.append(task_object)

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
    return tasks_list


def get_tasks(container_identifier=None):

    """Get all task() objects in a list

    :returns: list -- of pypelyne2.src.modules.task.task.Task() objects

    """

    task_objects = []
    tasks = parse_tasks(container_identifier)
    for task in tasks:
        # print project
        new_task_object = entitytask.EntityTask(task)
        task_objects.append(new_task_object)

    return task_objects
