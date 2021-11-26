import os
import sys
import threading
import time

from Box2D.examples.framework import (Framework, main)
from managers.EntityManager import EntityManager
from managers.PlayerManager import PlayerManager
from managers.NetworkManager import NetworkManager
from managers.GameManager import GameManager
from serverEntities.ServerEntity import ServerEntity


class CodeSTG(Framework):
    name = "codeSTG"
    description = "debugging GUI from Box2D example\n will be rewrote later"

    def __init__(self):
        super(CodeSTG, self).__init__()
        self.network_manager = NetworkManager()
        self.entity_manager = EntityManager(self.world, self.network_manager)
        self.player_manager = PlayerManager(self.entity_manager, self.network_manager)
        self.game_manager = GameManager(self.entity_manager, self.player_manager, self.network_manager)

    def Keyboard(self, key):
        self.player_manager.debugKeyDown(key)

    def KeyboardUp(self, key):
        self.player_manager.debugKeyUp(key)

    def PostSolve(self, contact, impulse):
        ft_a, ft_b = contact.fixtureA, contact.fixtureB
        body_a, body_b = ft_a.body, ft_b.body
        ud_a, ud_b = body_a.userData, body_b.userData
        if isinstance(ud_a, ServerEntity):
            ud_a.onContact(contact, impulse, ud_b)
        if isinstance(ud_b, ServerEntity):
            ud_b.onContact(contact, impulse, ud_a)

    def Step(self, settings):
        try:
            super().Step(settings)

            for e in self.entity_manager.getEntityList():
                try:
                    e.update()
                    x, y = self.renderer.to_screen(e.body.position)
                    self.DrawStringAt(x, y, e.__class__.__name__[6:])
                except Exception as err:
                    print(err)
            self.player_manager.update()
            self.entity_manager.update()
            self.game_manager.update()
            self.network_manager.update()
            self.network_manager.flush()
        except Exception as err:
            print(err)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main(CodeSTG)
