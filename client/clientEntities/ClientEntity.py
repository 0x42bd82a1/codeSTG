import pygame
from pygame.sprite import Sprite
from managers import UIManager


class ClientEntity(Sprite):
    texture_path = "./assets/images/entities/entity.png"
    src_image = pygame.image.load(texture_path)
    scale = 1

    def __init__(self):
        super().__init__()
        self._layer = 1
        self.pos_x = 0
        self.pos_y = 0
        self.angle = 0
        self.image = pygame.image.load(self.texture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.state = {'idx': 0,
                      'type': self.__class__.__name__[6:],
                      'alive': 1,
                      'hp': 0,
                      'mhp': 128,
                      'pos': (0, 0),
                      'ang': 0,
                      'lv': (0, 0),
                      'av': 0, }

    def setState(self, d: dict) -> None:
        for e in d:
            if e in self.state:
                self.state[e] = d[e]

    def update(self, *args, **kwargs) -> None:
        angle = self.state['ang']*180/3.14159
        self.image = pygame.transform.rotozoom(self.src_image, angle, UIManager.zoom * self.scale)
        self.rect.x = (self.state['pos'][0] - UIManager.cam_x) * UIManager.cur_ppm + UIManager.SCREEN_WEIGHT / 2
        self.rect.y = -(self.state['pos'][1] - UIManager.cam_y) * UIManager.cur_ppm + UIManager.SCREEN_HEIGHT / 2
        self.rect.x -= self.image.get_width() / 2
        self.rect.y -= self.image.get_height() / 2
        self.angle += 1

    def destroy(self):
        pass
