import pygame
from pygame.sprite import Group
from dungeoncrawler.constants import *
from dungeoncrawler.images import *
from dungeoncrawler.character import Character
from dungeoncrawler.weapon import Weapon
from dungeoncrawler.items import Item
from dungeoncrawler.world import World

pygame.init()
level = 3
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')
font = pygame.font.Font("dungeoncrawler/assets/fonts/AtariClassic.ttf", 20)

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.rect.centery -= 1
        if pygame.time.get_ticks() - self.start_time > TEXT_TICKS:
            self.kill()

    def draw(self, surface, world):
        if self.rect.colliderect(world.screen_rect):
            blit_rect = world.get_screen_position(self.rect)
            surface.blit(self.image, blit_rect)

heart_empty = scale_image(load_image('dungeoncrawler/assets/images/items/heart_empty'), ITEM_SCALE)
heart_half = scale_image(load_image('dungeoncrawler/assets/images/items/heart_half'), ITEM_SCALE)
heart_full = scale_image(load_image('dungeoncrawler/assets/images/items/heart_full'), ITEM_SCALE)
coin_images = []
for index in range(4):
    image = scale_image(load_image(f'dungeoncrawler/assets/images/items/coin_f{index}'), ITEM_SCALE)
    coin_images.append(image)
potion_image = [scale_image(load_image('dungeoncrawler/assets/images/items/potion_red'), ITEM_SCALE)]

current_score = -1
current_level = -1
coin_width = coin_images[0].get_width()
screen_mid = SCREEN_WIDTH >> 1
def draw_info():
    pygame.draw.rect(screen, pygame.Color('grey50'), (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, pygame.Color('white'), (0, 50), (SCREEN_WIDTH, 50))
    current = player.health
    for i in range(5):
        if current >= 20:
            screen.blit(heart_full, (10+i*50, 0))
        elif current >= 10:
            screen.blit(heart_half, (10+i*50, 0))
        else:
            screen.blit(heart_empty, (10+i*50, 0))
        current -= 20

    if current_level != level:
        level_text = font.render(f'-=[{level}]=-', True, pygame.Color('blue'))
        level_rect = level_text.get_rect()
        level_rect.centery = 25
        level_rect.centerx = screen_mid
    screen.blit(level_text, level_rect)

    if current_score != player.score:
        score_text = font.render(f':{player.score}', True, pygame.Color('blue'))
        score_rect = score_text.get_rect()
        score_rect.centery = 25
        score_rect.x = SCREEN_WIDTH - 80
    screen.blit(score_text, score_rect)

character_images = {}
for character in CHARACTER_TYPES:
    if character == 'elf':
        use_offset = True
    else:
        use_offset = False
    character_images[character] = []
    for index in range(len(ANIMATION_TYPES)):
        character_images[character].append(load_images(f'dungeoncrawler/assets/images/characters/{character}/{ANIMATION_TYPES[index]}/', use_offset))

weapon_images = {}
for weapon in WEAPONS:
    weapon_images[weapon] = scale_image(load_image(f'dungeoncrawler/assets/images/weapons/{weapon}'), WEAPON_SCALE)

player_moving_left = False
player_moving_right = False
player_moving_up = False
player_moving_down = False

bow = Weapon(weapon_images['bow'], weapon_images['arrow'])
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
score_coin = Item(SCREEN_WIDTH - 80 - coin_width, 25, ITEM_COIN, coin_images)
item_group = pygame.sprite.Group()

# world_data = [[-1] * LEVEL_COLS] * LEVEL_ROWS

with open(f"dungeoncrawler/levels/level{level}_data.csv", 'r', newline="") as level_file:
            data = level_file.readlines()
            world_data = [[int(number) for number in line.split(',')] for line in data]

tile_images = load_tiles('dungeoncrawler/assets/images/tiles/')

world = World()
world.process_data(world_data, tile_images)
for item in world.items:
    new_item = None
    if item.tile_type == 9:
        new_item = Item(item.rect.centerx, item.rect.centery, ITEM_COIN, coin_images)
    elif item.tile_type == 10:
        new_item = Item(item.rect.x, item.rect.y, ITEM_POTION, potion_image)
    if new_item:
        item_group.add(new_item)
player = Character(world.player.rect.x, world.player.rect.y, 100, MOVEMENT_SPEED, character_images['elf'])
mob_list = []
mob_index = ['imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']
for mob in world.mobs:
    new_mob = Character(mob.rect.centerx, mob.rect.centery, 100, 5, character_images[mob_index[mob.tile_type-12]])
    mob_list.append(new_mob)

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

    damage = player.update()
    arrow = bow.update(player, world)
    if damage != 0:
            damage = -damage
            damage_text = DamageText(player.rect.centerx, player.rect.y, damage, pygame.Color('green') if damage > 0 else pygame.Color('red'))
            damage_text_group.add(damage_text)
    if arrow:
        arrow_group.add(arrow)
    arrow_group.update(mob_list)
    for mob in mob_list:
        damage = mob.update()
        if damage != 0:
            damage = -damage
            damage_text = DamageText(mob.rect.centerx, mob.rect.top, damage, pygame.Color('green') if damage > 0 else pygame.Color('red'))
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(player)
    score_coin.update(None)
    world.update(player)

    world.draw(screen)
    player.draw(screen, world)
    bow.draw(screen, world)
    for item in item_group:
        item.draw(screen, world)
    for mob in mob_list:
        mob.draw(screen, world)
    for current_arrow in arrow_group:
        current_arrow.draw(screen, world)
    for damage in damage_text_group:
        damage.draw(screen, world)
    draw_info()
    score_coin.draw_fixed(screen)
    pygame.display.update()

pygame.quit()