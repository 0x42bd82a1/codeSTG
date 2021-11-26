from serverEntities.ServerProjectile import ServerProjectile


class ServerBullet1(ServerProjectile):
    vertices = [(0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1), (0.1, -0.1), ]

    def __init__(self, manager, **kwargs):
        super().__init__(manager, vertices=ServerBullet1.vertices, **kwargs)

    def doDamage(self, contact, impulse, obj) -> float:
        return 2.5