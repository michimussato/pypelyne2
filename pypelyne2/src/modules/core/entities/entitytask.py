import random

import pypelyne2.src.modules.core.entities.entity as entity
import pypelyne2.src.modules.core.parser.plugin.parse_plugins as parse_plugins


class EntityTask(entity.Entity):
    def __init__(self, plugin_object=None):
        super(EntityTask, self).__init__()

        # overrides of base classes
        self.entity_type = 'task'

        # the plugin associated with the task
        # self.entity_task_plugin = None
        self.entity_task_plugin = plugin_object or parse_plugins.get_plugins()[random.randint(0, len(
            parse_plugins.get_plugins()) - 1)].rand_arch

        # the outputs belonging to this task
        self.entity_task_outputs = set()

        # the outputs from other tasks that are piped into this task
        # [output_uuid, output_uuid, output_uuid]
        # [{task: uuid, outputs: [uuid, uuid, uuid]},
        #  {task: uuid, outputs: [uuid, uuid, uuid]}]
        self.entity_task_inputs = set()

