from managers.NetworkManager import NetworkManager
from clientEntities.ClientEntity import ClientEntity
import pygame
from mathUtils import *


class DebugController(object):
    texture_path = "./assets/images/ui/cursor_target.png"
    target_img = pygame.image.load(texture_path)

    def __init__(self, network_manager: NetworkManager, screen: pygame.Surface):
        self.network_manager = network_manager
        self.screen = screen

    def update(self, entity: ClientEntity):
        from managers import UIManager
        vec = (UIManager.mouse_x-entity.rect.x, -UIManager.mouse_y+entity.rect.y)
        dst = (vec[0]**2+vec[1]**2)**0.5
        ea = entity.state['ang']
        eav = entity.state['av']
        da = normalizeAngle(vec2Angle(vec)-ea)
        if da > pi:
            da = da - pi2
        opr = {'idx': entity.state['idx'], 'accR': da*2-eav*0.3,
               'accX': 0, 'accY': 0, 'fire': 0}
        if pygame.K_w in UIManager.pressed_keys:
            opr['accY'] += 1
        if pygame.K_s in UIManager.pressed_keys:
            opr['accY'] -= 1
        if pygame.K_a in UIManager.pressed_keys:
            opr['accX'] -= 1
        if pygame.K_d in UIManager.pressed_keys:
            opr['accX'] += 1
        if pygame.K_SPACE in UIManager.pressed_keys:
            opr['fire'] = 1
        self.network_manager.dataWrite(('update', opr))

        trg = (entity.rect.x + angle2Vec(ea)[0] * dst - self.target_img.get_width()/2,
               entity.rect.y - angle2Vec(ea)[1] * dst - self.target_img.get_height()/2)
        self.screen.blit(self.target_img, trg)
