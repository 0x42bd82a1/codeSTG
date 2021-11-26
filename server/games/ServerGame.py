from managers.EntityManager import EntityManager
from managers.PlayerManager import PlayerManager
from managers.NetworkManager import NetworkManager
import random


class ServerGame(object):

    def __init__(self, entity_manager: EntityManager, player_manager: PlayerManager, network_manager: NetworkManager):
        self.entity_manager = entity_manager
        self.player_manager = player_manager
        self.network_manager = network_manager
        self.world = self.entity_manager.world
        self.step_count = 0

        self.world.gravity = (0, 0)

    def update(self):
        self.step_count += 1

