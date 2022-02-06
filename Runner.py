import pygame
from sys import exit
from random import randint, choice
import time


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.falling = 0
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        if self.gravity < 13:
            self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300 and self.falling == 0: # 
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self): # getting called because of update
        self.player_input()
        self.apply_gravity()
        self.animation_state()



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100), y_pos))

    def animation_state(self):
        if type == 'fly': self.animation_index += 0.5
        else: self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
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
    surface_score = test_font.render(f'{current_time}', False, (64, 64, 64))
    rect_score = surface_score.get_rect(center=(score_x_pos, score_y_pos))
    screen.blit(surface_score, rect_score)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        return False
    else:
        return True


#falling = 1 he should fall 
#falling = 0 he should stay on the ground



pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('我的第一游戏')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_x_pos, sky_y_pos = 0, 0
ground_x_pos, ground_y_pos = 0, 300
score_x_pos, score_y_pos = 400, 50

# Environment: background and foreground
surface_sky = pygame.image.load('graphics/Sky.png').convert_alpha()
surface_sky_flip = pygame.image.load('graphics/Sky_flip.png').convert_alpha()
surface_ground = pygame.image.load('graphics/ground.png').convert_alpha()
surface_ground_flip = pygame.image.load('graphics/ground_flip.png').convert_alpha()

# Intro Screen
stand_player = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
stand_player = pygame.transform.rotozoom(stand_player, 0, 2)
rect_player_stand = stand_player.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(surface_sky, (sky_x_pos, sky_y_pos))
        screen.blit(surface_sky_flip, (sky_x_pos - 800, sky_y_pos))
        screen.blit(surface_ground, (ground_x_pos, ground_y_pos))
        screen.blit(surface_ground_flip, (ground_x_pos + 800, ground_y_pos))
        sky_x_pos += 1
        ground_x_pos -= 1
        if sky_x_pos == 801: sky_x_pos = 0  # loop sky
        if ground_x_pos < -800: ground_x_pos = 0  # loop ground
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision

        if not collision_sprite(): # check if collision, if it is then game-active - false\
            player.sprite.falling = 1
            # game_active = False
        if player.sprite.rect.bottom > 1000:
            game_active = False
            obstacle_group.empty()
            player.sprite.falling = 0


    else:
        # Fill game over screen
        screen.fill((94, 129, 162))
        screen.blit(stand_player, rect_player_stand)

        # Display score
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
