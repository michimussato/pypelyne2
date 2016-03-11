import pypelyne2.src.core.parser.resources.rtask.parse_rtasks as parse_rtasks


tasks = parse_rtasks.get_rtasks()

for task in tasks:
    print
    print
    print 'processing {0}'.format(task)
    print dir(task)
    for attribute in dir(task):
        print '%s == %s' % (attribute, getattr(task, attribute))
