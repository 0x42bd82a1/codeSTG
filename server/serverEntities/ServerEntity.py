import Box2D
from Box2D import b2Body
# import Box2D as b2d


class ServerEntity(object):
    """
    Attributes:
        vertices: A list of bivector decide polygon shape of entity.
        mask: A 16bit integer for collision filtering. 0x0001 for entities
              on the ground, 0x0002 for entities in the sky.
        is_dynamic: Literally.
        is_destructible: Literally.
        max_hitpoint: Synonym of health.
        impact_resistance: Give your entity a kinetic armor.
                           Can prevent entity damaged by pushing something
                           by setting a small value.
        destroy_delay: Frames before destroy when hitpoint drops to 0.
    """
    vertices = [(0.5, 0.5), (-0.5, 0.5), (-0.5, -0.5), (0.5, -0.5), ]
    mask = 0x0003
    is_dynamic = True
    is_destructible = True
    max_hitpoint = 128
    impact_resistance = 1
    destroy_delay = 0

    # TODO: need to be corrected at different frequency

    def __init__(self, manager, position=(0, 0), angle=0, density=1,
                 linearVelocity=(0, 0), vertices=vertices, **kwargs):
        self.manager = manager
        self.toDestroy = -1
        if self.is_dynamic:
            self.body = self.manager.world.CreateDynamicBody(
                position=position, angle=angle, linearVelocity=linearVelocity)
        else:
            self.body = self.manager.world.CreateStaticBody(
                position=position, angle=angle, linearVelocity=linearVelocity)
        self.body.CreatePolygonFixture(vertices=vertices, density=density,
                                       maskBits=self.mask)
        self.body.userData = self

        self.hitpoint = self.max_hitpoint
        self.states = {'idx': id(self),
                       'type': self.__class__.__name__[6:],
                       'alive': 1,
                       'hp': self.hitpoint,
                       'mhp': self.max_hitpoint,
                       'pos': tuple(self.body.position),
                       'ang': self.body.angle,
                       'lv': tuple(self.body.linearVelocity),
                       'av': self.body.angularVelocity,}

    def getStates(self) -> dict:
        self.states['hp'] = self.hitpoint
        self.states['pos'] = tuple(self.body.position)
        self.states['ang'] = self.body.angle
        self.states['lv'] = tuple(self.body.linearVelocity)
        self.states['av'] = self.body.angularVelocity
        return self.states

    def update(self):
        """
        Called each frame to update any entities.
        """
        # TODO: Don't know how to get a pointer or so... Never mind, it's just a prototype

        if self.toDestroy > 0:
            self.toDestroy -= 1
            self.states['toDestroy'] = self.toDestroy

    def onContact(self, contact: Box2D.b2Contact, impulse: Box2D.b2ContactImpulse, obj):
        """
        Do NOT create any body during a contact
        """
        if self.is_destructible:
            impact = max(impulse.normalImpulses)
            if impact > self.impact_resistance:
                self.hitpoint -= impact + self.impact_resistance

            from serverEntities.ServerProjectile import ServerProjectile
            if isinstance(obj, ServerProjectile):
                self.hitpoint -= obj.doDamage(contact, impulse, self)

            if self.hitpoint < 0:
                self.scheduleDestroy(self.destroy_delay)

    def scheduleDestroy(self, t: int):
        """
        Determine frames before destroy this entity
        """
        if self.toDestroy < 0 or 0 <= t < self.toDestroy:
            self.toDestroy = t

    def destroy(self):
        self.states['alive'] = 0
        self.manager.world.DestroyBody(self.body)
