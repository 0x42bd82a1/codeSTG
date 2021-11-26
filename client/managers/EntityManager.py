import os
import pygame
from importlib import import_module
from clientEntities.ClientEntity import ClientEntity
from managers.NetworkManager import NetworkManager
from typing import *


class EntityManager(object):

    def __init__(self, screen: pygame.Surface, network_manager: NetworkManager):
        self.screen = screen
        self.network_manager = network_manager
        self.entity_module = {}
        self.entity_pool: Dict[int, ClientEntity] = {}
        self.sprite_group = pygame.sprite.Group()

        for e in os.listdir("./clientEntities"):
            if e.startswith('Client') and e.endswith('.py'):
                e = e[:-3]
                mod = import_module('clientEntities.' + e)
                self.entity_module[e[6:]] = mod

    def getAvailableModule(self) -> dict:
        return self.entity_module

    def getEntityPool(self) -> list:
        return self.entity_pool

    def addEntity(self, idx: int, name: str, **kwargs) -> ClientEntity:
        try:
            if name not in self.entity_module:
                print(str(name) + " not defined")
                name = "Entity"                   # spawn a default entity instead
            entity = getattr(self.entity_module[name], "Client"+name)
            entity = entity(**kwargs)
            self.entity_pool[idx] = entity
            self.sprite_group.add(entity)
        except Exception as err:
            print(err)
            return None
        return entity

    def removeEntity(self, idx: int):
        try:
            self.entity_pool[idx].kill()
            self.entity_pool.pop(idx)
        except Exception as err:
            print(err)

    def update(self) -> None:
        """
        Warning, it will flush network buffer currently
        """
        try:
            d = self.network_manager.dataRead(flush=True)
            for e in d:
                try:
                    idx = e[2][1]['idx']
                    if e[2][0] == "destroy":
                        self.entity_pool[idx].setState({'alive': 0})
                        self.removeEntity(idx)
                    else:
                        if idx not in self.entity_pool:
                            self.entity_pool[idx] = self.addEntity(idx, e[2][1]['type'])
                        self.entity_pool[idx].setState(e[2][1])
                except Exception as err:
                    print(err)
            self.sprite_group.update()
            self.sprite_group.draw(self.screen)
        except Exception as err:
            print(err)
