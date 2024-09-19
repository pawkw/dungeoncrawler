import pygame
from pygame.sprite import Group
from dungeoncrawler.constants import *
from dungeoncrawler.character import Character
from dungeoncrawler.world import World

class Item(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, item_type: int, animation_list) -> None:
        super().__init__()
        self.item_type = item_type
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_list = animation_list
        self.image = animation_list[0]
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_length = len(self.animation_list)

    def update(self, player: Character):
        if self.animation_length > 1 and pygame.time.get_ticks() - self.update_time > ANIMATION_TICKS:
            self.frame_index = (self.frame_index + 1) % self.animation_length
            self.image = self.animation_list[self.frame_index]
            self.update_time = pygame.time.get_ticks()
        if player and self.rect.colliderect(player.rect):
            if self.item_type == ITEM_COIN:
                player.increase_score(1)
            elif self.item_type == ITEM_POTION:
                player.take_hit(-20)
            else:
                pass
            self.kill()

    def draw(self, surface: pygame.surface.Surface, world):
        if self.rect.colliderect(world.screen_rect):
            blit_rect = pygame.rect.Rect(self.rect)
            blit_rect.centerx = self.rect.centerx - world.screen_rect.left
            blit_rect.centery = self.rect.centery - world.screen_rect.top

            surface.blit(self.image, blit_rect)

    def draw_fixed(self, surface):
        surface.blit(self.image, self.rect)