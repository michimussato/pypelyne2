import pypelyne2.src.modules.core.parser.resources.rcontainer.parse_rcontainers as parse_rcontainers


containers = parse_rcontainers.get_rcontainers()

# print len(containers)

for container in containers:
    print container

for attr in dir(containers[0]):
    print attr, '=', getattr(containers[0], attr)
