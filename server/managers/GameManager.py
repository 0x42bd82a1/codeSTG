import os
from importlib import  import_module

from .EntityManager import EntityManager
from .PlayerManager import PlayerManager
from .NetworkManager import NetworkManager


class GameManager(object):
    def __init__(self, entity_manager: EntityManager, player_manager: PlayerManager, network_manager: NetworkManager):
        self.entity_manager = entity_manager
        self.player_manager = player_manager
        self.network_manager = network_manager
        self.game_module = {}
        self.current_game = None

        for e in os.listdir("./games"):
            if e.endswith('.py'):
                e = e[:-3]
                mod = import_module('games.' + e)
                self.game_module[e] = mod
        self.game_module.pop('ServerGame')
        self.game_module.pop('__init__')

        print(list(self.getAvailableModule().keys()))
        while self.current_game is None:
            name = input("Choose one to play:")
            self.startGame(name)

    def getAvailableModule(self) -> dict:
        return self.game_module

    def startGame(self, name: str, **kwargs):
        """
        Args:
            name: Name of game to init. List of names returned by getAvailableModule()
            kwargs: More args for game settings
        """
        try:
            if name not in self.game_module:
                print(str(name) + "not defined")
                return None
            game = getattr(self.game_module[name], name)
            game = game(entity_manager=self.entity_manager,
                        player_manager=self.player_manager,
                        network_manager=self.network_manager,
                        **kwargs)
        except Exception as err:
            print(err)
            return None
        self.current_game = game
        return game

    def update(self):
        if self.current_game is not None:
            try:
                self.current_game.update()
            except Exception as err:
                print(err)

