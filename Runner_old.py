import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    surface_score = test_font.render(f'{current_time}', False, (64, 64, 64))
    rect_score = surface_score.get_rect(center=(score_x_pos, score_y_pos))
    screen.blit(surface_score, rect_score)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


def player_animation():
    global player_surface, player_index

    if rect_player.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('我的第一游戏')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_x_pos, sky_y_pos = 0, 0
ground_x_pos, ground_y_pos = 0, 300
score_x_pos, score_y_pos = 400, 50
player_fall, player_x_pos = 0, 80
obst_x_start = 700

# Environment: background and foreground
surface_sky = pygame.image.load('graphics/Sky.png').convert_alpha()
surface_sky_flip = pygame.image.load('graphics/Sky_flip.png').convert_alpha()
surface_ground = pygame.image.load('graphics/ground.png').convert_alpha()
surface_ground_flip = pygame.image.load('graphics/ground_flip.png').convert_alpha()

# Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_surface = player_walk[player_index]
rect_player = player_surface.get_rect(midbottom=(80, 300))
gravity_player = 0

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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 900)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_player.bottom >= 300:
                    gravity_player = -20
            if rect_player.bottom >= 300 and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gravity_player = -20

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 210)))
            if event.type == snail_animation_timer:
                snail_frame_index = not snail_frame_index
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                # see about just doing fly_frame_index = not fly_frame_index
                fly_frame_index = not fly_frame_index
                fly_surface = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                rect_player.bottom, rect_player.left, player_fall = ground_y_pos, 100, 0
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(surface_sky, (sky_x_pos, sky_y_pos))
        screen.blit(surface_sky_flip, (sky_x_pos - 800, sky_y_pos))
        screen.blit(surface_ground, (ground_x_pos, ground_y_pos))
        screen.blit(surface_ground_flip, (ground_x_pos + 800, ground_y_pos))
        score = display_score()
        screen.blit(player_surface, rect_player)
        sky_x_pos += 1
        ground_x_pos -= 1
        if sky_x_pos == 801: sky_x_pos = 0  # loop sky
        if ground_x_pos < -800: ground_x_pos = 0  # loop ground

        # Player
        gravity_player += 1
        rect_player.y += gravity_player
        if rect_player.bottom >= 300 and player_fall == 0: rect_player.bottom = 300
        player_animation()
        screen.blit(player_surface, rect_player)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        if collisions(rect_player, obstacle_rect_list) is False:
            player_fall = 1
        if rect_player.bottom >= 1000: game_active = False

    else:
        # Reset obstacle list - prevent immediate collision upon restart
        obstacle_rect_list.clear()

        # Fill game over screen
        screen.fill((94, 129, 162))
        screen.blit(stand_player, rect_player_stand)

        # Display score
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)