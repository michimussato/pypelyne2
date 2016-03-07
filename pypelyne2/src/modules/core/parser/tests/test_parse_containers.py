import pypelyne2.src.modules.core.parser.parse_containers as parse_containers


containers = parse_containers.get_containers()

# print len(containers)

for container in containers:
    print container

for attr in dir(containers[0]):
    print attr, '=', getattr(containers[0], attr)
