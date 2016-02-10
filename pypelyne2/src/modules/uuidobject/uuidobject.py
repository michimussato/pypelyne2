import uuid


class UuidObject(object):
    def __init__(self, object_type=None, object_id=None):
        super(UuidObject, self).__init__()

        self.object_id = object_id or str(uuid.uuid4())

        self.object_type = object_type
