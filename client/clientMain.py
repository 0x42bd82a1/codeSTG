import os
os.chdir(os.path.dirname(__file__))
import pygame
import time
import managers.UIManager
from managers.NetworkManager import NetworkManager
from managers.UIManager import UIManager
from managers.EntityManager import EntityManager
from mathUtils import *

SCREEN_HEIGHT = managers.UIManager.SCREEN_HEIGHT
SCREEN_WEIGHT = managers.UIManager.SCREEN_WEIGHT
addr = None


class ClientMain(object):
    def __init__(self):

        global addr

        print("Hint:\n"
              "Left click to trace an entity.\n"
              "Right click to control a player if the owner is you.\n"
              "WSAD and space for controlling.\n"
              "LShift for an indicator.\n"
              "This program is just a GUI that need to connect a server to work\n")
        addr = input("server to connect:")
        if isValidIP(addr):
            addr = addr.split(':')
            addr = (addr[0], int(addr[1]))
        else:
            print("wtf did you type? I will use a default address instead.")
            addr = ('127.0.0.1', 4119)
        self.server_address = addr

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.network_manager = NetworkManager()
        self.entity_manager = EntityManager(self.screen, self.network_manager)
        self.ui_manager = UIManager(self.screen, self.entity_manager, self.network_manager)

        self.network_manager.connectPort(self.server_address)

    def update(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.ui_manager.processInput(event)

            self.screen.fill((32, 32, 32))
            self.network_manager.update()
            self.entity_manager.update()   # will flush buffer currently
            self.ui_manager.update()
            pygame.display.flip()
        except Exception as err:
            print(err)


if __name__ == '__main__':
    client = ClientMain()
    while True:
        client.clock.tick(60)
        client.update()
