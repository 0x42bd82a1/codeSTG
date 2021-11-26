import math

from .ServerRotor1 import ServerRotor1
from mathUtils import *


class ServerRotor1Hostile(ServerRotor1):
    def __init__(self, manager, **kwargs):
        super().__init__(manager,  **kwargs)
        self.trg_list = []
        self.owner = 'hostile bot'


    def update(self):
        self.trg_list.clear()
        for entity in self.manager.getEntityList():
            es = entity.getStates()
            if 'owner' in es and es['owner'] != self.owner:
                self.trg_list.append(es)

        trg = None
        tw = 65535
        sp = self.states['pos']
        sv = self.states['lv']
        sa = self.states['ang']
        for es in self.trg_list:
            p = es['pos']
            w = vec2Angle((p[0]-sp[0], p[1]-sp[1]))
            w = normalizeAngle(w - sa)
            if w > math.pi:
                w = pi2 - w
            w = w*9 + distance(p, sp)
            if w < tw:
                trg = es
                tw = w

        if trg is not None:
            p = trg['pos']
            v = trg['lv']
            v = (v[0]-sv[0], v[1]-sv[1])
            d = distance(p, sp)
            p = (p[0]+v[0]*d*0.03, p[1]+v[1]*d*0.03)
            w = vec2Angle((p[0] - sp[0], p[1] - sp[1]))
            w = normalizeAngle(w - sa)
            if w > math.pi:
                w = w - pi2
            fg = 1 if distance(sp, p) > 20 else -1
            self.inputs['accR'] = w*2
            self.inputs['accX'] = (p[0] - sp[0]) * fg
            self.inputs['accY'] = (p[1] - sp[1]) * fg
            if d < 40:
                self.inputs['fire'] = 1
            else:
                self.inputs['fire'] = 0
        else:
            self.inputs['accR'] = 0
            self.inputs['accX'] = 0
            self.inputs['accY'] = 0
            self.inputs['fire'] = 0

        super().update()
