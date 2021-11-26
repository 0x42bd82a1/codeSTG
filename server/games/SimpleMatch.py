from .ServerGame import ServerGame
from managers.EntityManager import EntityManager
from managers.PlayerManager import PlayerManager
from managers.NetworkManager import NetworkManager
import random


class SimpleMatch(ServerGame):

    def __init__(self, entity_manager: EntityManager, player_manager: PlayerManager, network_manager: NetworkManager):
        super().__init__(entity_manager, player_manager, network_manager)

        self.player1 = self.entity_manager.addEntity("Rotor1", position=(-10, 0))
        self.player_manager.bindPlayer(self.player1, ('127.0.0.1', 4119))
        self.player2 = self.entity_manager.addEntity("Rotor1", position=(10, 0))
        self.player_manager.bindPlayer(self.player2, ('127.0.0.1', 4110))
        print(id(self.player1))
        print(id(self.player2))
        print("a simple PVP between 2 rotors")
        self.p1_score = 0
        self.p2_score = 0

    def update(self):
        super().update()
        if not self.player1.states['alive']:
            self.p2_score += 1
            self.player1 = self.entity_manager.addEntity("Rotor1", position=(-10, 0))
            self.player_manager.bindPlayer(self.player1, ('127.0.0.1', 4119))
            print(self.p1_score, ':', self.p2_score)

        if not self.player2.states['alive']:
            self.p1_score += 1
            self.player2 = self.entity_manager.addEntity("Rotor1", position=(10, 0))
            self.player_manager.bindPlayer(self.player2, ('127.0.0.1', 4109))
            print(self.p1_score, ':', self.p2_score)
