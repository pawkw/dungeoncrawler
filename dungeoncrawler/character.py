import pygame
import math
from dungeoncrawler.constants import *
from dungeoncrawler.world import Tile
from typing import List

IDLE = 0
RUNNING = 1

class Character:
    diagonal = math.sqrt(2)/2

    def __init__(self, x: int, y: int, health: int, speed: int, animation_list: list, boss: bool = False) -> None:
        current_time = pygame.time.get_ticks()
        self.animation_list = animation_list
        self.flip = 0
        self.frame_index = 0
        self.action = IDLE
        self.image = self.animation_list[self.action][self.flip][self.frame_index]
        if boss:
            self.rect = self.image.get_rect()
        else:
            self.rect = pygame.rect.Rect(0, 0, ITEM_SIZE, ITEM_SIZE)
        self.rect.center = (x, y)
        self.speed = speed
        self.counter = 0
        self.health_max = health
        self.health = health
        self.last_update = current_time
        self.damage = 0
        self.alive = True
        self.score = 0
        self.target_coord = None
        self.attack_time = current_time
        self.stunned_time = current_time

    def move(self, x: int, y: int, world) -> None:
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
        obstacle = world.check_obstacle_collsions(self.rect)
        if obstacle:
            if dx > 0:
                self.rect.right = obstacle.rect.left
            else:
                self.rect.left = obstacle.rect.right

        self.rect.y += dy
        obstacle = world.check_obstacle_collsions(self.rect)
        if obstacle:
            if dy > 0:
                self.rect.bottom = obstacle.rect.top
            else:
                self.rect.top = obstacle.rect.bottom

    def AI(self, player, mobs, world):
        if not self.alive:
            return
    
        current_time = pygame.time.get_ticks()
        if current_time - self.stunned_time < MOB_STUN_COOLDOWN:
            return
        
        line_to_player = (self.rect.center, player.rect.center)
        can_see_player = True
        for obstacle in world.obstacle_tiles:
            if obstacle.rect.clipline(line_to_player):
                can_see_player = False
        
        if can_see_player:
            self.target_coord = player.rect.center

        if self.rect.center == self.target_coord:
            self.target_coord = None

        if not self.target_coord:
            return
            
        dx = self.target_coord[0] - self.rect.centerx
        dy = self.target_coord[1] - self.rect.centery
        ai_dx = dx//abs(dx) if dx else 0
        ai_dy = dy//abs(dy) if dy else 0

        collision = self.rect.colliderect(player.rect)
        if collision:
            if current_time - self.attack_time > MOB_ATTACK_COOLDOWN:
                self.attack_time = current_time
                player.take_hit(15)
            return
        
        for mob in mobs:
            if self != mob and mob.action == RUNNING and self.rect.colliderect(mob.rect):
                collision = True
                self.action = IDLE
                break

        if not collision:           
            self.move(ai_dx, ai_dy, world)


    def take_hit(self, damage: int):
        self.stunned_time = pygame.time.get_ticks()
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
            self.action = IDLE
