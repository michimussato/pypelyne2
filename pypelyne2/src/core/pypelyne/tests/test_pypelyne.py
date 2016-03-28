import pypelyne2.src.core.pypelyne.pypelyne as pypelyne


p = pypelyne.Pypelyne()


print 'projects:                 ', p.projects
print 'all entities:             ', p.entities
# print 'all containers only:      ', p.containers()
print 'project ontainers only:   ', p.containers(project=list(p.projects)[0].identifier)
print 'Tasks only:               ', p.tasks

# print list(p.containers())[0].rcontainer.container_type
# print list(p.containers())[0].rcontainer.container_icon
#
# print list(p.tasks)[0].rplugin.executable
