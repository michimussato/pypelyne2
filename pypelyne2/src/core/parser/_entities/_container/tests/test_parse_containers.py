import pypelyne2.src.core.parser._entities._container.parse_containers as parse_containers


containers = parse_containers.get_containers(project_identifier=None)
# containers = parse_containers.get_containers(project_identifier='47d2d555-71c4-4921-a40a-6c9b0d5ec1f3')
# containers = parse_containers.get_containers(project_identifier='e3dfd1e5-f411-4cd4-97a2-53af38830493')

for container in containers:
    print
    print
    print 'processing {0}'.format(container)
    print dir(container)
    for attribute in dir(container):
        print '%s == %s' % (attribute, getattr(container, attribute))

print containers
