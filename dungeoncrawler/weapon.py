import pygame
from dungeoncrawler.character import Character
import math

class Weapon:
    def __init__(self, image) -> None:
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()

    def update(self, character: Character):
        self.rect.center = character.rect.center

        pos = pygame.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(dy, dx))

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, 
                    ((self.rect.centerx - int(self.image.get_width() >> 1),
                      self.rect.centery - int(self.image.get_height() >> 1)))
                      )