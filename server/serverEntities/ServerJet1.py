from .ServerPlayer import ServerPlayer
from mathUtils import *


class ServerJet1(ServerPlayer):
    mask = 0x0003
    max_hitpoint = 64
    impact_resistance = 1
    max_thrust = 100
    max_torque = 10
    max_gun_heat = 6
    linearDamping = 2.5
    angularDamping = 6

    def __init__(self, manager, **kwargs):
        super().__init__(manager, vertices=self.vertices, **kwargs)
        self.inputs = {'accX': 0, 'accY': 0, 'accR': 0, 'fire': 0}
        self.body.linearDamping = self.linearDamping
        self.body.angularDamping = self.angularDamping
        self.gun_heat = 0

    def onContact(self, contact, impulse, obj):
        super().onContact(contact, impulse, obj)

    def update(self):
        super().update()

        body = self.body
        acc = self.inputs['accY']
        if acc > 1:
            acc = 1
        if acc < 0:
            acc = 0
        force = acc * self.max_thrust * angle2Vec(self.body.angle)
        body.ApplyForce(force, body.GetWorldPoint((0, 0)), True)

        acc = self.inputs['accR']
        acc = constrain(acc, -1, 1)
        torque = acc * self.max_torque
        body.ApplyTorque(torque, True)

        if self.inputs['fire'] > 0 and self.gun_heat < 1:
            self.simpleShoot(bullet="Bullet1", speed=40)
            self.gun_heat = self.max_gun_heat

        if self.gun_heat > 0:
            self.gun_heat -= 1
