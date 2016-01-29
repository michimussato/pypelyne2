import json
import logging
import operator
import pypelyne2.src.modules.task.task as class_task
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


def parse_tasks():
    logging.info('parsing tasks')

    with open(SETTINGS.TASKS_FILE, 'r') as f:
        json_object = json.load(f)
    # f.close()

    tasks = [task for task in json_object if task['task_enable']]

    return sorted(tasks,
                  key=operator.itemgetter(SETTINGS.SORT_TASKS),
                  reverse=SETTINGS.SORT_TASKS_REVERSE)


def get_tasks():
    task_objects = []
    tasks = parse_tasks()
    print tasks
    for task in tasks:
        new_task_object = class_task.Task(task)
        task_objects.append(new_task_object)

    return task_objects
