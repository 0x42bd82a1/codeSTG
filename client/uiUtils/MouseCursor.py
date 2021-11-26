import pygame
from pygame.sprite import Sprite


class MouseCursor(Sprite):

    texture_path = "./assets/images/ui/cursor.png"
    cursor_image = pygame.image.load(texture_path)

    def __init__(self):
        super().__init__()
        self._layer = 2
        self.pos_x = 0
        self.pos_y = 0
        self.angle = 0
        self.scale = 1
        self.image = self.cursor_image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs) -> None:
        self.image = pygame.transform.rotozoom(self.cursor_image, self.angle, self.scale)
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        self.rect.x -= self.image.get_width()/2
        self.rect.y -= self.image.get_height()/2
        # self.angle += 1

