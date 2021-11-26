from .ClientPlayer import ClientPlayer
import pygame


class ClientRotor1Hostile(ClientPlayer):
    texture_path = "./assets/images/entities/rotor1_r.png"
    src_image = pygame.image.load(texture_path)
