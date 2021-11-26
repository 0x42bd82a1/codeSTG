from .ClientPlayer import ClientPlayer
import pygame


class ClientJet1(ClientPlayer):
    texture_path = "./assets/images/entities/jet1.png"
    src_image = pygame.image.load(texture_path)
