import Box2D
from managers.NetworkManager import NetworkManager
from serverEntities.ServerEntity import ServerEntity
from serverEntities.ServerPlayer import ServerPlayer
from importlib import import_module
import os
import gc


class EntityManager(object):

    def __init__(self, world: Box2D.b2World, network_manager: NetworkManager):
        """
        Imports modules named as "serverXxx.py" at initialization
        """
        self.world = world
        self.network_manager = network_manager
        self.entity_pool = []
        self.entity_module = {}
        # TODO: need more efficient structure

        for e in os.listdir("./serverEntities"):
            if e.startswith('Server') and e.endswith('.py'):
                e = e[:-3]
                mod = import_module('serverEntities.' + e)
                self.entity_module[e[6:]] = mod

    def getAvailableModule(self) -> dict:
        return self.entity_module

    def getEntityList(self) -> list:
        return self.entity_pool

    def addEntity(self, name: str, **kwargs) -> ServerEntity:
        """
        Args:
            name: Name of entity to spawn. List of names returned by getAvailableModule()
            kwargs: Most args are used by b2Body.
        Returns:
            The entity it spawned.
        """
        try:
            if name not in self.entity_module:
                print(str(name) + " not defined")
                return None
            entity = getattr(self.entity_module[name], "Server"+name)
            entity = entity(manager=self, **kwargs)
            self.entity_pool.append(entity)
        except Exception as err:
            print(err)
            return None
        self.network_manager.dataWrite(('new', entity.getStates()))
        # print(('new', entity.getStates()))
        return entity

    def destroyEntity(self, trg_entity: ServerEntity):
        """
        Do NOT use
        Use destroy() of entity itself instead, for it may cause some problem.
        """
        # FIXME: delete it later
        assert isinstance(trg_entity, ServerEntity)
        for i, entity in enumerate(self.entity_pool):
            if entity == trg_entity:
                self.entity_pool.pop(i)
                if isinstance(entity, ServerPlayer):
                    # self.player_manager.unbindPlayer(id(entity))
                    # FIXME: piece of shit.
                    # FIXME: need GC.
                    pass
                # TODO: self.network_manager ...
                entity.destroy()

    def update(self):
        for i, entity in enumerate(self.entity_pool):
            if entity.toDestroy == 0:
                self.entity_pool.pop(i)
                if isinstance(entity, ServerPlayer):
                    # self.player_manager.unbindPlayer(id(entity))
                    pass
                self.network_manager.dataWrite(('destroy', {'idx': id(entity)}))
                entity.destroy()
            else:
                self.network_manager.dataWrite(('update', entity.getStates()))
