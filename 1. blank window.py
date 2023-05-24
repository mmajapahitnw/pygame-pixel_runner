import pygame
from sys import exit
from random import randint

def obstacle_movement(obstacle_list):
    if obstacle_list:   # check if list is not empty
        for obstacle in obstacle_list:
            obstacle.x -= 5

            if obstacle.bottom == 300:
                screen.blit(snail_surf, obstacle)
            else:
                screen.blit(fly_surf, obstacle)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right >= 0]

        return obstacle_list

    else:
        return []

def collisions(obstacles, player):
    if collisions:
        for rectangle in obstacles:
            if player.colliderect(rectangle):
                return False
    return True

def display_score():
    # global current_time

    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)

    return current_time

def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

pygame.init()       # starts pygame

width = 800
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()     # it gives a clock object

game_active = False
start_time = 0
score = 0

# sky_surface = pygame.Surface((100, 200))
# sky_surface.fill('cyan')

sky_surface = pygame.image.load('graphics/Sky.png').convert()   # to convert into more friendly type of image
ground_surface = pygame.image.load('graphics/ground.png').convert()  # makes the game more efficient

text_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # (font type, font size), None = default type
# score_surface = text_font.render('My game', False, (64, 64, 64))  # (the text, anti-aliasing, color)
# score_rectangle = score_surface.get_rect(center=(400, 50))

snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # alpha to remove the strange bits
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_index = 0
snail_surf = snail_frames[snail_index]
# snail_rectangle = snail_surface.get_rect(bottomleft=(800, 300))

fly_frame1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstacle_rect_list = []

player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_surface = player_walk[player_index]
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
# player_rectangle = pygame.Rect(left=,right=,top=,bottom=) to fit into certain sized rect
# rect allows us to place surface with different anchor point, and also ti enable collision
player_rectangle = player_surface.get_rect(midbottom=(80, 300))    # draws a rect around a surface

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
# player_stand = pygame.transform.scale2x(player_stand)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

game_name = text_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rectangle = game_name.get_rect(center=(400, 70))

game_message = text_font.render('Press  [spacebar]  to run', False, 'white')
game_message_rectangle = game_message.get_rect(center=(400, 340))

player_gravity = 0

# timer
obstacle_timer = pygame.USEREVENT + 1  # there are some event that already reserved for pygame itself
pygame.time.set_timer(obstacle_timer, 1500)  # in ms
snail_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_anim_timer, 500)
fly_anim_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_anim_timer, 200)

while True:
    # draw all elements
    # update everything

    for event in pygame.event.get():       # will return list of all events
        if event.type == pygame.QUIT:
            pygame.quit()   # the opposite of init
            exit()  # delete while true loop

        if game_active:
            # if event.type == pygame.MOUSEMOTION:
            #     print(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                    player_gravity = -20
            # if event.type == pygame.MOUSEBUTTONUP:
            #     print('mouse released')
            # if event.type == pygame.MOUSEMOTION:  # to check collision player with mouse cursor
            #     if player_rectangle.collidepoint(event.pos):
            #         print('collide')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomleft=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomleft=(randint(900, 1100), 210)))

            if event.type == snail_anim_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surf = snail_frames[snail_index]

            if event.type == fly_anim_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frames[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rectangle.left = 800
                start_time = int(pygame.time.get_ticks()/1000)



    if game_active:
        score = display_score()

        screen.blit(sky_surface, (0, 0))   # to put another surface on this surface (x, y)
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 0, 5)    # width, border_rounding
        # pygame.draw.line(screen, 'red', (0,0), pygame.mouse.get_pos(), 6)
        # pygame.draw.ellipse(screen, 'brown', pygame.Rect(50, 200, 100, 100))  # (left, top, width, height)
        # screen.blit(score_surface, score_rectangle)
        display_score()

        player_animation()
        screen.blit(player_surface, player_rectangle)
        # player_rectangle.left += 1 alternative way to move surface, or rect
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # screen.blit(snail_surface, snail_rectangle)
        # snail_rectangle.x -= 5
        # if snail_rectangle.right <= 0:
        #     snail_rectangle.left = 800

        game_active = collisions(obstacle_rect_list, player_rectangle)

        # mouse_pos = pygame.mouse.get_pos()  # gets position of mouse in (x,y)
        # if player_rectangle.collidepoint((mouse_pos)):
        #     print('collision')

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(game_name, game_name_rectangle)

        obstacle_rect_list.clear()
        player_rectangle.bottom = 300
        player_gravity = 0
        player_index = 0

        score_surface = text_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_rectangle = score_surface.get_rect(center=(400, 340))

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_surface, score_rectangle)


    pygame.display.update()
    clock.tick(60)      # to ensure that the while loop run at 60 times per second max
