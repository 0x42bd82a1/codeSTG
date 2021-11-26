from .ClientEntity import ClientEntity
import pygame


class ClientBullet1(ClientEntity):
    texture_path = "./assets/images/entities/bullet1.png"
    src_image = pygame.image.load(texture_path)