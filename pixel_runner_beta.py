import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.walk = [player_walk1, player_walk2]
        self.walk_index = 0
        self.image = self.walk[self.walk_index]     # this HAS to be self.image
        self.jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100, 300))       # this HAS to be self.rect
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.4)    # between 0 - 1

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.walk_index += 0.1
            if self.walk_index >= len(self.walk):
                self.walk_index = 0
            self.image = self.walk[int(self.walk_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()  # to access the parent init

        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]

    def destroy(self):
        global score
        if self.rect.right <= 0:
            score += 1
            self.kill()     # destroy said sprite

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):       # (sprite, group, bool)
    # the bool determine whether the group member gets deleted after colliding with the sprite
        obstacle_group.empty()  # delete every sprite member
        return False
    else:
        return True

def display_score(score):

    score_surface = text_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)

pygame.init()       # starts pygame

width = 800
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()     # it gives a clock object

game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)    # loops forever

player = pygame.sprite.GroupSingle()    # create a group single
player.add(Player())    # add sprite object into group

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()   # to convert into more friendly type of image
ground_surface = pygame.image.load('graphics/ground.png').convert()  # makes the game more efficient

text_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # (font type, font size), None = default type

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

game_name = text_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rectangle = game_name.get_rect(center=(400, 70))

game_message = text_font.render('Press  [spacebar]  to run', False, 'white')
game_message_rectangle = game_message.get_rect(center=(400, 340))

player_gravity = 0

# timer
obstacle_timer = pygame.USEREVENT + 1  # there are some event that already reserved for pygame itself
pygame.time.set_timer(obstacle_timer, 1500)  # in ms

while True:
    # draw all elements
    # update everything

    for event in pygame.event.get():       # will return list of all events
        if event.type == pygame.QUIT:
            pygame.quit()   # the opposite of init
            exit()  # delete while true loop

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                score = 0

    if game_active:
        screen.blit(sky_surface, (0, 0))   # to put another surface on this surface (x, y)
        screen.blit(ground_surface, (0, 300))

        display_score(score)

        player.draw(screen)     # display the sprite
        player.update()     # update the sprite

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(game_name, game_name_rectangle)
        player.sprite.rect.bottom = 300
        player.sprite.gravity = 0

        score_surface = text_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_rectangle = score_surface.get_rect(center=(400, 340))

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_surface, score_rectangle)

    pygame.display.update()
    clock.tick(60)      # to ensure that the while loop run at 60 times per second max
