import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.parser.parse_containers as parse_containers


containers = parse_containers.get_containers()

# print len(containers)

for container in containers:
    print container

for attr in dir(containers[0]):
    print attr, '=', getattr(containers[0], attr)
