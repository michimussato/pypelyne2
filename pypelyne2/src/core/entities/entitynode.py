import pypelyne2.src.core.entities.entity as entity


class EntityNode(entity.Entity):

    """Documentation for class Node(Entity)."""

    def __init__(self):

        super(EntityNode, self).__init__()

        self.connections = dict()
