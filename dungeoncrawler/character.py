import pygame
import math
from dungeoncrawler.constants import *

IDLE = 0
RUNNING = 1

class Character:
    diagonal = math.sqrt(2)/2

    def __init__(self, x: int, y: int, health: int, speed: int, animation_list: list) -> None:
        self.animation_list = animation_list
        self.flip = 0
        self.frame_index = 0
        self.action = IDLE
        self.image = self.animation_list[self.action][self.flip][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.counter = 0
        self.health_max = health
        self.health = health
        self.last_update = pygame.time.get_ticks()
        self.damage = 0
        self.alive = True
        self.score = 0

    def move(self, x: int, y: int, obstacle_tiles) -> None:
        if x == 0 and y == 0:
            self.action = IDLE
            return
        self.action = RUNNING
        dx = x*self.speed
        dy = y*self.speed
        if dx != 0 and dy != 0:
            dx *= self.diagonal
            dy *= self.diagonal
        
        if dx < 0:
            self.flip = 1
        elif dx > 0:
            self.flip = 0
        
        self.rect.x += dx
        

        self.rect.y += dy

    def take_hit(self, damage: int):
        self.damage = damage

    def increase_score(self, score: int):
        self.score += score

    def update(self):
        current_time = pygame.time.get_ticks()
        result = self.damage
        self.image = self.animation_list[self.action][self.flip][self.frame_index]
        # center = self.rect.center
        # self.rect = self.image.get_rect()
        # self.rect.center = center
        if self.damage != 0:
            self.health -= self.damage
            self.damage = 0
        if self.health <= 0:
            self.alive = False
        if self.health > self.health_max:
            self.health = self.health_max
        if current_time - self.last_update > ANIMATION_TICKS and self.alive:
            self.frame_index = (self.frame_index + 1) & 3
            self.last_update = current_time
        return result

    #def draw(self, surface):
        # surface.blit(self.image, self.rect)
        # pygame.draw.rect(surface, pygame.Color('red'), self.rect, 1)

    def draw(self, surface: pygame.surface.Surface, world):
        if self.rect.colliderect(world.screen_rect):
            blit_rect = world.get_screen_position(self.rect)
            surface.blit(self.image, blit_rect)
            pygame.draw.rect(surface, pygame.Color('red'), blit_rect, 1)
