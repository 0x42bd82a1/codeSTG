import Box2D

from serverEntities.ServerEntity import ServerEntity


class ServerProjectile(ServerEntity):
    max_hitpoint = 0.1
    impact_resistance = 0
    max_lifetime = 60

    # TODO: need to be corrected at different frequency

    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.body.bullet = True
        self.body.density = 4
        self.lifetime = self.max_lifetime

    def onContact(self, contact, impulse, obj):
        super().onContact(contact, impulse, obj)

    def doDamage(self, contact: Box2D.b2Contact, impulse: Box2D.b2ContactImpulse, obj: ServerEntity) -> float:
        """
        Args:
            contact: A b2Contact.
            impulse: A b2ContactImpulse.
            obj: Entity this projectile hits.
        Returns:
            A float to deal damage directly.
        """
        # obj.hitpoint -= 65535
        # return 65535


    def update(self):
        super().update()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.scheduleDestroy(0)
