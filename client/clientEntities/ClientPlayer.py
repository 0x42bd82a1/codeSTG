from .ClientEntity import ClientEntity
import pygame


class ClientPlayer(ClientEntity):
    texture_path = "./assets/images/entities/entity.png"
    src_image = pygame.image.load(texture_path)

    def __init__(self):
        super().__init__()
        self.state.update({'owner': None})
