# usage:

import src.parser.parse_tasks as parse_tasks

tasks = parse_tasks.get_tasks()

attributes = dir(tasks[0])
for attribute in attributes:
    print '%s = %s' % (attribute, getattr(tasks[1], attribute))
