import pypelyne2.src.core.parser._entities._project.parse_projects as parse_projects


projects = parse_projects.get_projects()

# print projects

for project in projects:
    print
    print
    print 'processing {0}'.format(project)
    print dir(project)
    for attribute in dir(project):
        print '%s == %s' % (attribute, getattr(project, attribute))

print projects
