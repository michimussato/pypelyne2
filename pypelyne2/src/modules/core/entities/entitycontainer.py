import pypelyne2.src.modules.core.entities.entity as entity


class EntityContainer(entity.Entity):
    def __init__(self):
        super(EntityContainer, self).__init__()

        # overrides of base classes
        self.entity_type = 'container'

        # all tasks that are contained in this container
        self.entity_container_tasks = set()

        # # the outputs belonging to this container
        # self.entity_container_outputs = set()
        #
        # # the outputs from other containers that are piped into this container
        # # [output_uuid, output_uuid, output_uuid]
        # # [{container: uuid, tasks: [uuid, uuid, uuid]},
        # #  {task: uuid, outputs: [uuid, uuid, uuid]}]
        # self.entity_container_inputs = set()
