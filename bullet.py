import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """对飞船发射子弹管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """creat a bullet object"""
        super().__init__()
        self.screen = screen

        # first create a bullet at position (0, 0), then set the right position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # save position of the bullet
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    def update(self):
        """move the bullet up"""
        # renew the float y number of the bullet
        self.y -= self.speed
        # renew the y number use the float self.y
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet on the screen"""
        # update its position
        # self.update() 在update_bullets中调用了
        # draw the bullet self
        pygame.draw.rect(self.screen, self.color, self.rect)
