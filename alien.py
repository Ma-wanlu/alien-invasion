import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """represents a single alien object"""

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the image of alien
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # place alien at the up left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # float number save the position of alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """check if the alien touch the edge of screen"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += self.ai_settings.alien_move_right_or_left * self.ai_settings.direction
        self.rect.x = self.x

    # def blitme(self):
    #     """draw alien"""
    #     self.update()
    #     self.screen.blit(self.image, self.rect)
