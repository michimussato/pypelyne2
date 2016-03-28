# import pypelyne2.src.core.parser.entities.parse_entities as parse_entities
# import pypelyne2.src.core.parser.resources.rcontainer.parse_rcontainers as parse_rcontainers
# import pypelyne2.src.core.parser.resources.routput.parse_routputs as parse_routputs
# import pypelyne2.src.core.parser.resources.rplugin.parse_rplugins as parse_rplugins
# import pypelyne2.src.core.parser.resources.rtask.parse_rtasks as parse_rtasks
import pypelyne2.src.core.parser.projects.parse_projects as parse_projects


projects = parse_projects.get_projects()

for project in projects:
    print
    print
    print 'processing {0}'.format(project)
    print dir(project)
    for attribute in dir(project):
        print '%s == %s' % (attribute, getattr(project, attribute))


print
print
print 'entities found:'
print projects
