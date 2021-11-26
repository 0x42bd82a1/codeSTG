import pygame
from clientEntities.ClientEntity import ClientEntity
from managers.EntityManager import EntityManager
from managers.NetworkManager import NetworkManager
from managers.DebugController import DebugController
from uiUtils.MouseCursor import MouseCursor
from collections import Iterable
from mathUtils import *

SCREEN_HEIGHT = 480
SCREEN_WEIGHT = 600
MAX_SCALE = 1
MIN_SCALE = 0.05
PPM = 48  # pixel per meter
# 48 pixels for 1 unit in this game
# not parts per million
zoom = 0.5
cur_ppm = 24
mouse_x = 0
mouse_y = 0
pressed_keys = set()
cam_x = 0
cam_y = 0
trace_entity: ClientEntity = None
control_entity: ClientEntity = None


class UIManager(object):
    global zoom
    global cur_ppm
    global mouse_x
    global mouse_y
    global cam_x
    global cam_y
    global trace_entity

    def __init__(self, screen: pygame.Surface, entity_manager: EntityManager, network_manager: NetworkManager):
        self.screen = screen
        self.entity_manager = entity_manager
        self.network_manager = network_manager
        self.debug_controller = DebugController(network_manager, screen)
        pygame.mouse.set_visible(False)
        self.cursor_sprite = MouseCursor()
        # self.scale_indicator =
        self.ui_group = pygame.sprite.Group()
        self.ui_group.add(self.cursor_sprite)

        self.trg_cam_x = 0
        self.trg_cam_y = 0

    def isFriendly(self, entity: ClientEntity):
        if 'owner' not in entity.state or not isinstance(entity.state['owner'], Iterable):
            return False
        return tuple(entity.state['owner']) == self.network_manager.addr

    def cameraZoom(self, key):
        global zoom
        global PPM
        global cur_ppm
        if key == 5:
            zoom *= 0.9
        if key == 4:
            zoom *= 1.11
        if zoom > MAX_SCALE:
            zoom = MAX_SCALE
        if zoom < MIN_SCALE:
            zoom = MIN_SCALE
        cur_ppm = PPM * zoom

    def cameraMove(self):
        global pressed_keys
        global mouse_x
        global mouse_y
        global zoom
        global cam_x
        global cam_y
        if trace_entity:
            self.trg_cam_x, self.trg_cam_y = trace_entity.state['pos']
        else:
            if pygame.K_a in pressed_keys:
                self.trg_cam_x -= 0.5 / zoom
            if pygame.K_d in pressed_keys:
                self.trg_cam_x += 0.5 / zoom
            if pygame.K_w in pressed_keys:
                self.trg_cam_y += 0.5 / zoom
            if pygame.K_s in pressed_keys:
                self.trg_cam_y -= 0.5 / zoom
        cam_x += (self.trg_cam_x - cam_x) * 0.1 + (mouse_x - SCREEN_WEIGHT/2) / cur_ppm / 10
        cam_y += (self.trg_cam_y - cam_y) * 0.1 - (mouse_y - SCREEN_HEIGHT/2) / cur_ppm / 10

    def mouseUpdate(self):
        global mouse_x
        global mouse_y
        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.SysFont('', 24)
        ep = self.entity_manager.entity_pool
        for idx in ep:
            e = ep[idx]
            if pygame.sprite.collide_rect(self.cursor_sprite, e):
                if 'owner' in e.state:
                    txt = str(e.state['owner'])
                    clr = (255, 192, 0) if self.isFriendly(e) else (255, 0, 0)
                    text = font.render(txt, 1, clr)
                    self.screen.blit(text, (e.rect.x + 16, e.rect.y - 32))
                if 'mhp' in e.state and e.state['mhp'] > 1:
                    txt = str(int(e.state['hp']))+'/'+str(int(e.state['mhp']))
                    text = font.render(txt, 1, (255, 140, 0))
                    self.screen.blit(text, (e.rect.x+16, e.rect.y-16))

    def mouseButtonDown(self, event):
        global mouse_x
        global mouse_y
        global trace_entity
        global control_entity
        ep = self.entity_manager.entity_pool
        if event.button == 1 or event.button == 3:
            if trace_entity:
                trace_entity = None
                control_entity = None
            for idx in ep:
                ei = ep[idx]
                if pygame.sprite.collide_rect(self.cursor_sprite, ei):
                    trace_entity = ei
                    if event.button == 3 and self.isFriendly(ei):
                        control_entity = ei
                    break

    def mouseButtonUp(self, event):
        pass

    def processInput(self, event):
        global pressed_keys
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5:
                self.cameraZoom(event.button)
            self.mouseButtonDown(event)
        if event.type == pygame.KEYDOWN:
            pressed_keys.add(event.key)
        if event.type == pygame.KEYUP:
            pressed_keys.discard(event.key)

    def update(self):
        global trace_entity
        global control_entity
        global cam_x
        global cam_y
        try:
            self.cameraMove()
            self.mouseUpdate()
            self.cursor_sprite.update()
            self.ui_group.update()
            self.ui_group.draw(self.screen)
        except Exception as err:
            print(err)

        try:
            ep = self.entity_manager.entity_pool
            if pygame.K_LSHIFT in pressed_keys:
                for idx in ep:
                    ei = ep[idx]
                    if 'owner' in ei.state:
                        ex, ey = ei.state['pos']
                        ex = (ex-cam_x)*0.5
                        ey = -(ey-cam_y)*0.5
                        cx = SCREEN_WEIGHT / 2
                        cy = SCREEN_HEIGHT / 2
                        clr = (255, 192, 0) if self.isFriendly(ei) else (255, 0, 0)
                        pygame.draw.line(self.screen, clr, (cx, cy), (cx + ex, cy + ey), 1)

            if trace_entity is not None:
                if trace_entity.state['alive']:
                    pygame.draw.rect(self.screen, (255, 192, 0), (0, 0, 256, 16), 3)
                    mhp = trace_entity.state['mhp']
                    hp = trace_entity.state['hp']
                    pygame.draw.line(self.screen, (255, 192, 0), (0, 8), ((min(hp, mhp) / mhp) * 256, 8), 16)
                    font = pygame.font.SysFont('', 24)
                    txt = str(int(hp)) + '/' + str(int(mhp))
                    text = font.render(txt, 1, (255, 192, 0))
                    self.screen.blit(text, (0, 24))
                else:
                    trace_entity = None
                    control_entity = None

            if control_entity is not None:
                self.debug_controller.update(control_entity)

        except Exception as err:
            print(err)

