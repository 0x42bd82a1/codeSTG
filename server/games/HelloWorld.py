from .ServerGame import ServerGame
from managers.EntityManager import EntityManager
from managers.PlayerManager import PlayerManager
from managers.NetworkManager import NetworkManager
import random


class HelloWorld(ServerGame):

    def __init__(self, entity_manager: EntityManager, player_manager: PlayerManager, network_manager: NetworkManager):
        super().__init__(entity_manager, player_manager, network_manager)
        
        boundary = self.world.CreateStaticBody(position=(0, 20))
        boundary.CreateEdgeChain([(-30, -30), (-30, 30), (30, 30), (30, -30), (-30, -30)], )
        e = self.entity_manager.addEntity("Rotor1", position=(10, 10))
        self.player_manager.debugBindPlayer(e)
        e = self.entity_manager.addEntity("Rotor1", position=(-10, 10))
        self.player_manager.bindPlayer(e, ('127.0.0.1', 4119))
        print(id(e))
        e.hitpoint = 65535
        self.entity_manager.addEntity("Rotor1Hostile", position=(-20, 20))
        for i in range(10):
            self.entity_manager.addEntity("Box", position=(i * 2, 0))

    def update(self):
        super().update()
        """
        if self.step_count % 1 == 0:
            for i in range(10):
                self.entity_manager.addEntity("ServerBullet1",
                                              position=(random.randrange(-30, 30),
                                                     random.randrange(-10, 50)))
        """
