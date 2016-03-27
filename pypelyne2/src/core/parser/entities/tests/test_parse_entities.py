import pypelyne2.src.core.parser.entities.parse_entities as parse_entities
import pypelyne2.src.core.parser.resources.rcontainer.parse_rcontainers as parse_rcontainers
import pypelyne2.src.core.parser.resources.routput.parse_routputs as parse_routputs
import pypelyne2.src.core.parser.resources.rplugin.parse_rplugins as parse_rplugins
import pypelyne2.src.core.parser.resources.rtask.parse_rtasks as parse_rtasks

entities = parse_entities.get_entities(rplugins=parse_rplugins.get_rplugins(),
                                       rcontainers=parse_rcontainers.get_rcontainers(),
                                       rtasks=parse_rtasks.get_rtasks(),
                                       routputs=parse_routputs.get_routputs())

for entity in entities:
    print
    print
    print 'processing {0}'.format(entity)
    print dir(entity)
    for attribute in dir(entity):
        print '%s == %s' % (attribute, getattr(entity, attribute))


print
print
print 'entities found:'
print entities
