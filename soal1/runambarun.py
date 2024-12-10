import pygame
from sys import exit
from random import randint, choice
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/bocchi/meme4.jpeg')
        self.player_walk = [player_walk_1]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/bocchi/meme5.jpg')

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(120, 400))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.115)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 400:
            self.gravity = -23.5
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 0.87
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400

    def animation_state(self):
        if self.rect.bottom < 400:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':
            bat_1 = pygame.image.load('graphics/bat/bat1.png')
            bat_2 = pygame.image.load('graphics/bat/bat2.png')
            bat_3 = pygame.image.load('graphics/bat/bat3.png')
            self.frames = [bat_1, bat_2, bat_3]
            y_pos = 250
        else:
            ghost_1 = pygame.image.load('graphics/ghost/ghost1.png')
            ghost_2 = pygame.image.load('graphics/ghost/ghost2.png')
            self.frames = [ghost_1, ghost_2]
            y_pos = 400

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (174, 184, 230))
    score_rect = score_surf.get_rect(center=(center_x, center_y - 180))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

pygame.init()
screen_width, screen_height = 1000, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Run Amba Run')
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
center_x, center_y = screen_width // 2, screen_height // 2

bg_music = pygame.mixer.Sound('audio/bocchi.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load('graphics/sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
tree_surface = pygame.image.load('graphics/tree.png').convert_alpha()
scroll1 = scroll2 = 0

# Intro screen
player_stand = pygame.image.load('graphics/bocchi/meme6.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(screen_width // 2, screen_height // 2))
game_name = test_font.render('Run Amba Run', False, (69, 100, 255))
game_name_rect = game_name.get_rect(center=(screen_width // 2, screen_height // 2 - 130))
game_message = test_font.render('Press space to run', False, (69, 100, 255))
game_message_rect = game_message.get_rect(center=(screen_width // 2, screen_height // 2 + 130))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bat', 'ghost', 'ghost', 'ghost'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Background layers
        screen.blit(sky_surface, (0, 0))
        for i in range(-1, screen_width // tree_surface.get_width() + 2):
            screen.blit(tree_surface, (tree_surface.get_width() * i + scroll1, 0))
        scroll1 = (scroll1 - 1) % tree_surface.get_width()

        for i in range(-1, screen_width // ground_surface.get_width() + 2):
            screen.blit(ground_surface, (ground_surface.get_width() * i + scroll2, 400))
        scroll2 = (scroll2 - 5) % ground_surface.get_width()

        # Player and Obstacles
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision detection
        game_active = collision_sprite()

        # Score display
        score = display_score()

    else:
        # Game over screen
        screen.fill((0, 0, 0))
        screen.blit(player_stand, player_stand_rect)
        obstacle_group.empty()
        player.sprite.rect.midbottom = (120, 400)
        player.sprite.gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (121, 142, 247))
        score_message_rect = score_message.get_rect(center=(screen_width // 2, screen_height // 2 + 130))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)