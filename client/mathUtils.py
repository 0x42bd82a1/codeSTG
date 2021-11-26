import math
from math import *
from functools import *
import re

eps = 1e-6
pi2: float = math.pi * 2


def isValidIP(addr: str) -> bool:
    addr = addr.strip().split(':')
    if len(addr) != 2 or not addr[1].isdigit():
        return False
    addr[1] = int(addr[1])
    if addr[1] < 1024 or addr[1] > 65535:
        return False
    compile_ip = re.compile(r'^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{'
                            r'2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    return compile_ip.match(addr[0]) is not None


def norm(vec):
    return reduce(lambda x, y: x + y ** 2, vec) ** 0.5


def normalize(vec):
    tmp = norm(vec)
    if tmp == 0:
        return tuple([0] * len(vec))
    return tuple(map(lambda x: x / tmp, vec))


def distance(va, vb):
    return ((vb[0]-va[0])**2+(vb[1]-va[1])**2)**0.5


def angle2Vec(x: float) -> tuple:
    return cos(x), sin(x)


def vec2Angle(vec) -> float:
    return math.atan2(vec[1], vec[0])


def normalizeAngle(x: float) -> float:
    x = math.fmod(x, pi2)
    if x < 0:
        x += pi2
    return x
