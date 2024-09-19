from dungeoncrawler.constants import *
# from dungeoncrawler.character import Character
import pygame
from dataclasses import dataclass
import csv

@dataclass
class Tile:
    def __init__(self, tile_type, image, image_rect):
        self.tile_type = tile_type
        self.image = image
        self.rect = image_rect

class World:
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.items = []
        self.exit_tile = None
        self.player = None
        self.mobs = []
        self.world_map = pygame.surface.Surface((LEVEL_COLS * TILE_SIZE, LEVEL_ROWS * TILE_SIZE))
        self.world_map.fill(BACKGROUND_COLOUR)
        self.rect = self.world_map.get_rect()
        self.screen_rect = pygame.rect.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def process_data(self, data, tile_image_list):
        self.level_length = len(data)

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image: pygame.surface.Surface = tile_image_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.left = image_x
                image_rect.top = image_y
                if tile == 7:
                    self.obstacle_tiles.append(Tile(tile, image, image_rect))
                elif tile == 8:
                    self.exit_tile = Tile(tile, image, image_rect)
                elif tile == 9 or tile == 10:
                    self.items.append(Tile(tile, image, image_rect))
                    tile = 0
                    image: pygame.surface.Surface = tile_image_list[tile]
                elif tile == 11:
                    self.player = Tile(tile, image, image_rect)
                    tile = 0
                    image: pygame.surface.Surface = tile_image_list[tile]
                elif tile > 11:
                    self.mobs.append(Tile(tile, image, image_rect))
                    tile = 0
                    image: pygame.surface.Surface = tile_image_list[tile]
                
                if tile >= 0:
                    self.map_tiles.append(Tile(tile, image, image_rect))
                    self.world_map.blit(image, (image_x, image_y))

    def get_screen_position(self, item_rect):
        relative_rect = pygame.rect.Rect(item_rect)
        relative_rect.centerx = item_rect.centerx - self.screen_rect.left
        relative_rect.centery = item_rect.centery - self.screen_rect.top
        return relative_rect
    
    def get_world_postion(self, item_rect):
        absolute_rect = pygame.rect.Rect(item_rect)
        absolute_rect.left += self.screen_rect.left
        absolute_rect.top += self.screen_rect.top
        return absolute_rect
    
    def check_obstacle_collsions(self, item_rect: pygame.rect.Rect):
        for obstacle in self.obstacle_tiles:
            if item_rect.colliderect(obstacle.rect):
                return obstacle
        return None

    def update(self, player):
        if player.rect.left < self.screen_rect.left + SCROLL_THRESHOLD:
            self.screen_rect.left = player.rect.left - SCROLL_THRESHOLD
        if player.rect.right > self.screen_rect.right - SCROLL_THRESHOLD:
            self.screen_rect.right = player.rect.right + SCROLL_THRESHOLD
        if player.rect.top < self.screen_rect.top + SCROLL_THRESHOLD:
            self.screen_rect.top = player.rect.top - SCROLL_THRESHOLD
        if player.rect.bottom > self.screen_rect.bottom - SCROLL_THRESHOLD:
            self.screen_rect.bottom = player.rect.bottom + SCROLL_THRESHOLD

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.world_map, (0, 0), self.screen_rect)