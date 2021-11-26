from serverEntities.ServerEntity import ServerEntity


class ServerBox(ServerEntity):
    mask = 0x0003

    linearDamping = 8
    angularDamping = 8
    max_hitpoint = 16

    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.body.linearDamping = ServerBox.linearDamping
        self.body.angularDamping = ServerBox.angularDamping

    def onContact(self, contact, impulse, obj):
        super().onContact(contact, impulse, obj)
