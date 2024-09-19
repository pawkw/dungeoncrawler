from typing import Any
import pygame
from pygame.sprite import Group
from dungeoncrawler.character import Character
import math
from dungeoncrawler.constants import *
from dungeoncrawler.world import World
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

    def update(self, character: Character, world):
        self.rect.center = character.rect.center

        pos = pygame.mouse.get_pos()
        screen_position = world.get_screen_position(self.rect)
        dx = pos[0] - screen_position.centerx
        dy = -(pos[1] - screen_position.centery)
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
        
    def draw(self, surface: pygame.surface.Surface, world):
        if self.rect.colliderect(world.screen_rect):
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            blit_rect = pygame.rect.Rect(self.rect)
            blit_rect.centerx = self.rect.centerx - world.screen_rect.left
            blit_rect.centery = self.rect.centery - world.screen_rect.top

            surface.blit(self.image, ((blit_rect.centerx - int(self.image.get_width() >> 1),
                                       blit_rect.centery - int(self.image.get_height() >> 1)))
                    )
        
class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x: int, y: int, angle: float) -> None:
        super().__init__()
        self.angle = angle - 90
        self.image = pygame.transform.rotate(image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.angle + 90)) * SHOT_SPEED
        self.dy = -math.sin(math.radians(self.angle + 90)) * SHOT_SPEED
        self.distance = SHOT_DISTANCE

    def update(self, mob_list, world: World) -> None:
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.distance -= 1

        if self.distance <= 0 or world.check_obstacle_collsions(self.rect):
            self.kill()

        for mob in mob_list:
            if mob.alive and mob.rect.colliderect(self.rect):
                damage = 10 + random.randint(-5, 5)
                mob.take_hit(damage)
                self.kill()
                break

    def draw(self, surface, world):
        if self.rect.colliderect(world.screen_rect):
            blit_rect = pygame.rect.Rect(self.rect)
            blit_rect.centerx = self.rect.centerx - world.screen_rect.left
            blit_rect.centery = self.rect.centery - world.screen_rect.top
            
            surface.blit(self.image, 
                    ((blit_rect.centerx - int(self.image.get_width() >> 1),
                      blit_rect.centery - int(self.image.get_height() >> 1)))
                      )