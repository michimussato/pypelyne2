import pypelyne2.src.core.pypelyne.pypelyne as pypelyne


p = pypelyne.Pypelyne()


projects = p.get_projects()
# print projects
print ''
print 'projects------------------------'
for i in p.get_projects():
    print i.identifier, i
    # print i.identifier

# p.reload()
# # entities = p.entities()
#
# # print 'projects:                 ', [x.identifier for x in projects]
# # print list(projects)[0].identifier
# # print 'all entities:             ', entities
# # print 'all containers only:      ', p.containers()
# # print 'project ontainers only:   ', p.containers(project=list(projects)[0].identifier)
# # print 'project ontainers only:   ', p.containers(project='47d2d555-71c4-4921-a40a-6c9b0d5ec1f3')
# # print 'Tasks only:               ', p.tasks
#
#
print ''
print 'entities------------------------'
# for i in p.get_entities(projects=[x.identifier for x in p.get_projects()]):
# for i in p.get_entities():
# for i in p.get_entities(projects=['47d2d555-71c4-4921-a40a-6c9b0d5ec1f3']):
# for i in p.get_entities(projects=['e3dfd1e5-f411-4cd4-97a2-53af38830493']):
for i in p.get_entities(projects=['47d2d555-71c4-4921-a40a-6c9b0d5ec1f3', 'e3dfd1e5-f411-4cd4-97a2-53af38830493'],
                        entity_types=['all']):
# for i in p.get_entities(projects=p.get_projects()):
# for i in p.containers():
    print i
#
# p.reload()
#
# print ''
# print 'containers----------------------'
# # for i in p.get_containers(projects=['e3dfd1e5-f411-4cd4-97a2-53af38830493']):
# # for i in p.containers(projects=['47d2d555-71c4-4921-a40a-6c9b0d5ec1f3', 'e3dfd1e5-f411-4cd4-97a2-53af38830493']):
# # for i in p.containers(projects=projects):
# # for i in p.containers(projects=[x.identifier for x in projects]):
# for i in p.get_containers():
#     print i.identifier, i
#     print
#
# p.reload()
#
# print ''
# print 'tasks---------------------------'
# # for i in p.tasks(projects=['e3dfd1e5-f411-4cd4-97a2-53af38830493']):
# for i in p.get_tasks(projects=['47d2d555-71c4-4921-a40a-6c9b0d5ec1f3']):
# # for i in p.containers(projects=['47d2d555-71c4-4921-a40a-6c9b0d5ec1f3', 'e3dfd1e5-f411-4cd4-97a2-53af38830493']):
# # for i in p.containers(projects=projects):
# # for i in p.containers(projects=[x.identifier for x in projects]):
# # for i in p.containers():
#     print i
#     print i.identifier
#
# p.reload()
#
# print 'outputs---------------------------'
# # for i in p.tasks(projects=['e3dfd1e5-f411-4cd4-97a2-53af38830493']):
# for i in p.get_outputs(projects=['47d2d555-71c4-4921-a40a-6c9b0d5ec1f3']):
# # for i in p.containers(projects=['47d2d555-71c4-4921-a40a-6c9b0d5ec1f3', 'e3dfd1e5-f411-4cd4-97a2-53af38830493']):
# # for i in p.containers(projects=projects):
# # for i in p.containers(projects=[x.identifier for x in projects]):
# # for i in p.containers():
#     print i
#     print i.identifier
#
# p.reload()
#
# # print list(p.containers())[0].rcontainer.container_type
# # print list(p.containers())[0].rcontainer.container_icon
# #
# # print list(p.tasks)[0].rplugin.executable
