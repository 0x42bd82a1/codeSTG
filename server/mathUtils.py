import math
from math import *
from functools import *
from Box2D import b2Vec2
from Box2D import b2Vec3

eps = 1e-6
pi2: float = math.pi * 2


def norm(vec):
    if isinstance(vec, b2Vec2):
        return (vec.x**2+vec.y**2)**0.5
    if isinstance(vec, tuple) or isinstance(vec, list):
        return reduce(lambda x, y: x+y**2, vec)**0.5


def distance(va, vb):
    return ((vb[0]-va[0])**2+(vb[1]-va[1])**2)**0.5


def normalize(vec):
    if isinstance(vec, b2Vec2):
        if vec == b2Vec2(0, 0):
            return b2Vec2(0, 0)
        return vec/(vec.x**2+vec.y**2)**0.5
    if isinstance(vec, tuple):
        tmp = norm(vec)
        if tmp == 0:
            return tuple([0] * len(vec))
        return tuple(map(lambda x: x/tmp, vec))

    if isinstance(vec, list):
        tmp = norm(vec)
        if tmp == 0:
            return [0] * len(vec)
        return list(map(lambda x: x / tmp, vec))


def constrain(x, minimum, maximum):
    if x > maximum:
        return maximum
    if x < minimum:
        return minimum
    return x


def angle2Vec(x: float) -> b2Vec2:
    return b2Vec2(cos(x), sin(x))


def vec2Angle(vec) -> float:
    return math.atan2(vec[1], vec[0])


def normalizeAngle(x: float) -> float:
    x = math.fmod(x, pi2)
    if x < 0:
        x += pi2
    return x
