import pypelyne2.src.core.parser._entities._task.parse_tasks as parse_tasks


tasks = parse_tasks.get_tasks()

# print projects

for task in tasks:
    print
    print
    print 'processing {0}'.format(task)
    print dir(task)
    for attribute in dir(task):
        print '%s == %s' % (attribute, getattr(task, attribute))

print tasks
