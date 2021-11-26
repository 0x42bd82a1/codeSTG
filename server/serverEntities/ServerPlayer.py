from serverEntities.ServerEntity import ServerEntity
from mathUtils import *


class ServerPlayer(ServerEntity):
    """
    Attributes:
        inputs: A dict to store inputs. Will be checked each frame.
    """

    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.inputs = {}
        self.owner = None
        self.states.update({'owner': self.owner, })

    def onContact(self, contact, impulse, obj):
        super().onContact(contact, impulse, obj)

    def setInput(self, inputs):
        for k in inputs:
            if k in self.inputs:
                self.inputs[k] = inputs[k]

    def simpleShoot(self, bullet="Bullet1", speed=20):
        body = self.body
        ang = body.angle
        pos = body.position + angle2Vec(ang) * 0.75
        vel = body.linearVelocity + angle2Vec(ang) * speed
        self.manager.addEntity(bullet, position=pos, linearVelocity=vel,
                               angle=ang)
        pass

    def getStates(self) -> dict:
        self.states['owner'] = self.owner
        return super().getStates()

    def update(self):
        super().update()
        if self.hitpoint < 0:
            self.scheduleDestroy(2)
