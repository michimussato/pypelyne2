import pypelyne2.src.core.pypelyne.pypelyne as pypelyne


p = pypelyne.Pypelyne()

print 'all entities:   ', p.entities
print 'projects only:  ', p.projects
print 'Containers only:', p.containers
print 'Tasks only:     ', p.tasks

print list(p.containers)[0].rcontainer.container_type
print list(p.containers)[0].rcontainer.container_icon

print list(p.tasks)[0].rplugin.executable
