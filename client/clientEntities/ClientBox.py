from .ClientEntity import ClientEntity
import pygame


class ClientBox(ClientEntity):
    texture_path = "./assets/images/entities/box.png"
    src_image = pygame.image.load(texture_path)