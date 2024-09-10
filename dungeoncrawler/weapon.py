from typing import Any
import pygame
from pygame.sprite import Group
from dungeoncrawler.character import Character
import math
from dungeoncrawler.constants import *
import random

class Weapon:
    def __init__(self, image, ammo_image) -> None:
        self.original_image = image
        self.ammo_image = ammo_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.last_fired = 0
        self.fired = False

    def update(self, character: Character):
        self.rect.center = character.rect.center

        pos = pygame.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(dy, dx))

        arrow = None
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and not self.fired and (current_time - self.last_fired) > SHOT_COOLDOWN:
            arrow = Arrow(self.ammo_image, self.rect.centerx, self.rect.centery, self.angle)
            self.last_fired = current_time
            self.fired = True
        
        if self.fired and pygame.mouse.get_pressed()[0] == False:
            self.fired = False

        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, 
                    ((self.rect.centerx - int(self.image.get_width() >> 1),
                      self.rect.centery - int(self.image.get_height() >> 1)))
                      )
        
class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x: int, y: int, angle: float) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle - 90
        self.image = pygame.transform.rotate(image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.angle + 90)) * SHOT_SPEED
        self.dy = -math.sin(math.radians(self.angle + 90)) * SHOT_SPEED
        self.distance = SHOT_DISTANCE

    def update(self, mob_list) -> None:
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.distance -= 1

        if self.distance <= 0:
            self.kill()

        for mob in mob_list:
            if mob.alive and mob.rect.colliderect(self.rect):
                damage = 10 + random.randint(-5, 5)
                mob.take_hit(damage)
                self.kill()
                break

    def draw(self, surface):
        surface.blit(self.image, 
                    ((self.rect.centerx - int(self.image.get_width() >> 1),
                      self.rect.centery - int(self.image.get_height() >> 1)))
                      )