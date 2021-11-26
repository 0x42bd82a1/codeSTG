from .ServerGame import ServerGame
from managers.EntityManager import EntityManager
from managers.PlayerManager import PlayerManager
from managers.NetworkManager import NetworkManager
import random


class Intro(ServerGame):

    def __init__(self, entity_manager: EntityManager, player_manager: PlayerManager, network_manager: NetworkManager):
        super().__init__(entity_manager, player_manager, network_manager)

        self.player1 = self.entity_manager.addEntity("Rotor1", position=(-10, 0))
        self.player_manager.bindPlayer(self.player1, ('127.0.0.1', 4119))
        self.player2 = self.entity_manager.addEntity("Jet1", position=(10, 0))
        self.player_manager.bindPlayer(self.player2, ('127.0.0.1', 4119))
        print(id(self.player1))
        print(id(self.player2))
        self.player1.hitpoint = 2147483648
        self.player2.hitpoint = 2147483648

        print("Waiting for connection on 192.168.0.1:4119")
        print("Test enemy will be spawned when there's someone connecting")
        print("1 simple rotor and 3 boxes spawned each 10 second")

        self.fg = 1

    def update(self):
        super().update()
        if self.step_count % 596 == 0 and self.network_manager.connection_count > 0:
            x, y = (self.player2.states['pos'] if self.fg > 0 else self.player2.states['pos'])
            self.fg *= -1
            self.entity_manager.addEntity("Rotor1Hostile", position=(x + 20, y + 20))
            self.entity_manager.addEntity("Box", position=(x - 20, y + 20))
            self.entity_manager.addEntity("Box", position=(x + 20, y - 20))
            self.entity_manager.addEntity("Box", position=(x - 20, y - 20))

