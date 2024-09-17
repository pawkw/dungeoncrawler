import pygame
import math
from dungeoncrawler.constants import *

IDLE = 0
RUNNING = 1

class Character:
    diagonal = math.sqrt(2)/2

    def __init__(self, x: int, y: int, health: int, speed: int, animation_list: list) -> None:
        self.animation_list = animation_list
        self.image = animation_list[0]
        self.flip = 0
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.rect.center = (x, y)
        self.frame_index = 0
        self.speed = speed
        self.counter = 0
        self.action = IDLE
        self.health_max = health
        self.health = health
        self.last_update = pygame.time.get_ticks()
        self.damage = 0
        self.alive = True
        self.score = 0

    def move(self, x: int, y: int) -> None:
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

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, pygame.Color('red'), self.rect, 1)
