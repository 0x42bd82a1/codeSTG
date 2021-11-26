from .ClientPlayer import ClientPlayer
import pygame


class ClientRotor1(ClientPlayer):
    texture_path = "./assets/images/entities/rotor1.png"
    src_image = pygame.image.load(texture_path)
