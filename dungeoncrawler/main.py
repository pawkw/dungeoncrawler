import pygame
from pygame.sprite import Group
from dungeoncrawler.constants import *
from dungeoncrawler.images import *
from dungeoncrawler.character import Character
from dungeoncrawler.weapon import Weapon
from dungeoncrawler.items import Item

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')
font = pygame.font.Font("dungeoncrawler/assets/fonts/AtariClassic.ttf", 20)

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.rect.centery -= 1
        if pygame.time.get_ticks() - self.start_time > TEXT_TICKS:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

heart_empty = scale_image(load_image('dungeoncrawler/assets/images/items/heart_empty'), ITEM_SCALE)
heart_half = scale_image(load_image('dungeoncrawler/assets/images/items/heart_half'), ITEM_SCALE)
heart_full = scale_image(load_image('dungeoncrawler/assets/images/items/heart_full'), ITEM_SCALE)
coin_images = []
for index in range(4):
    image = scale_image(load_image(f'dungeoncrawler/assets/images/items/coin_f{index}'), COIN_SCALE)
    coin_images.append(image)
potion_image = [scale_image(load_image('dungeoncrawler/assets/images/items/potion_red'), ITEM_SCALE)]

current_score = -1
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

    if current_score != player.score:
        score_text = font.render(f':{player.score}', True, pygame.Color('blue'))
        score_rect = score_text.get_rect()
        score_rect.centery = 25
        score_rect.x = screen_mid + coin_width
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

player = Character(100, 100, 100, MOVEMENT_SPEED, character_images['elf'])
player_moving_left = False
player_moving_right = False
player_moving_up = False
player_moving_down = False
player.take_hit(25)

bow = Weapon(weapon_images['bow'], weapon_images['arrow'])
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
potion = Item(200, 200, ITEM_POTION, potion_image)
coin = Item(250, 200, ITEM_COIN, coin_images)
score_coin = Item(screen_mid + (coin_width >> 1), 25, ITEM_COIN, coin_images)
item_group = pygame.sprite.Group()
item_group.add(potion)
item_group.add(coin)

mob_list = []
enemy = Character(200, 300, 300, MOVEMENT_SPEED, character_images['imp'])
mob_list.append(enemy)

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
    arrow = bow.update(player)
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
            damage_text = DamageText(mob.rect.centerx, mob.rect.y, damage, pygame.Color('green') if damage > 0 else pygame.Color('red'))
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(player)
    score_coin.update(None)

    player.draw(screen)
    bow.draw(screen)
    item_group.draw(screen)
    for mob in mob_list:
        mob.draw(screen)
    arrow_group.draw(screen)
    damage_text_group.draw(screen)
    draw_info()
    score_coin.draw(screen)
    pygame.display.update()

pygame.quit()