import pygame
from pygame.locals import *
from sys import exit

if __name__ == '__main__':
    background_image = './assets/images/background.png'
    mouse_image = './assets/images/jet1.png'
    angle = 0  # 设置角度
    clock = pygame.time.Clock()
    x = 0
    y = 0
    angle = 0
    # 初始化pygame，为使用硬件做准备
    pygame.init()
    # 创建了一个窗口
    screen = pygame.display.set_mode((480, 700), 0, 32)
    # 设置窗口标题
    pygame.display.set_caption("hello world")

    # 加载并转换图像
    background = pygame.image.load(background_image).convert()
    mouse_cursor = pygame.image.load(mouse_image).convert_alpha()


    while True:
        clock.tick(60)  # 设置帧率

        for event in pygame.event.get():
            if event.type == QUIT:  # 接收到退出事件后退出程序
                exit()
        screen.blit(background, (0, 0))  # 画上背景图

        angle += 1
        x += 1
        y += 1

        # mouse_rect = mouse_cursor.get_rect()


        x, y = pygame.mouse.get_pos()  # 获得鼠标位置
        # 计算光标左上角位置
        x -= mouse_cursor.get_width()/2
        y -= mouse_cursor.get_height()/2
        #画上光标
        mouse_cursor = pygame.image.load('./assets/images/jet1.png')# 再次导入图片
        mouse_cursor = pygame.transform.rotate(mouse_cursor, angle)#选择
        screen.blit(mouse_cursor, (x, y))



        # 刷新画面
        pygame.display.update()
