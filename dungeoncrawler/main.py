import pygame
from dungeoncrawler.constants import *
from dungeoncrawler.images import *
from dungeoncrawler.character import Character
from dungeoncrawler.weapon import Weapon

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

character_images = {}
for character in CHARACTER_TYPES:
    if character == 'elf':
        use_offset = True
    else:
        use_offset = False
    character_images[character] = []
    for index in range(len(ANIMATION_TYPES)):
        character_images[character].append(load_images(f'dungeoncrawler/assets/images/characters/{character}/{ANIMATION_TYPES[index]}', use_offset))

weapon_images = {}
for weapon in WEAPONS:
    weapon_images[weapon] = scale_image(load_image(f'dungeoncrawler/assets/images/weapons/{weapon}'), WEAPON_SCALE)

player = Character(100, 100, 100, MOVEMENT_SPEED)
player.set_images(character_images['elf'])
player_moving_left = False
player_moving_right = False
player_moving_up = False
player_moving_down = False
bow = Weapon(weapon_images['bow'])

run = True
while run:
    clock.tick(FRAME_RATE)
    screen.fill(BACKGROUND_COLOUR)
    
    dx = 0
    dy = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_moving_left = True
            if event.key == pygame.K_d:
                player_moving_right = True
            if event.key == pygame.K_w:
                player_moving_up = True
            if event.key == pygame.K_s:
                player_moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_moving_left = False
            if event.key == pygame.K_d:
                player_moving_right = False
            if event.key == pygame.K_w:
                player_moving_up = False
            if event.key == pygame.K_s:
                player_moving_down = False
    if player_moving_up:
        dy = -1
    if player_moving_down:
        dy = 1
    if player_moving_left:
        dx = -1
    if player_moving_right:
        dx = 1
    player.move(dx, dy)
    
    player.update()
    player.draw(screen)
    bow.update(player)
    bow.draw(screen)
    pygame.display.update()

pygame.quit()