import pygame
import random

# leaderboard
# splatoon
# attack enemy

pygame.init()

is_running = True
is_playing = True

# window
pygame.display.set_caption("Dino")
pygame.display.set_icon(pygame.image.load('media/dino.png'))

# font
font = pygame.font.Font('media/font/GOUDYSTO.TTF')
font_large = pygame.font.Font("media/font/GOUDYSTO.TTF", 60)

# time
clock = pygame.time.Clock()
start_time = 0

# display
display = pygame.display.set_mode((800,400))

# background
background = pygame.image.load('media/graphics/environment/sky.png')
background_rect_1 = background.get_rect(bottomleft=(0,400))
background_rect_2 = background.get_rect(bottomleft=background_rect_1.bottomright)

DEFAULT_BACKGROUND_SPEED = 4
background_speed = DEFAULT_BACKGROUND_SPEED

# platform
platform = pygame.image.load('media/graphics/environment/ground.png')
platform_rect_1 = platform.get_rect(bottomleft=(0,400))
platform_rect_2 = platform.get_rect(bottomleft=platform_rect_1.bottomright)

DEFAULT_PLATFORM_SPEED = 6
MAX_PLATFORM_SPEED =  20
platform_speed = DEFAULT_PLATFORM_SPEED

GROUND_Y = 300

# foreground
foreground = pygame.image.load('media/graphics/environment/foreground.png')

# player
player_walk_1 = pygame.image.load('media/graphics/characters/player/player_walk_1.png')
player_walk_2 = pygame.image.load('media/graphics/characters/player/player_walk_2.png')
player_walk_3 = pygame.image.load('media/graphics/characters/player/player_walk_3.png')
player_walk_4 = pygame.image.load('media/graphics/characters/player/player_walk_4.png')
player_walk = [player_walk_1,player_walk_2, player_walk_3, player_walk_4]

player_crouch = pygame.image.load('media/graphics/characters/player/player_crouch.png')

player_surf = pygame.image.load('media/graphics/characters/player/player.png')
player_rect = player_surf.get_rect(bottomleft=(50, GROUND_Y))

player_grav = 0
PLAYER_MAX_GRAV = -20
PLAYER_DEF_GRAV = -17

# enemies
enemy_1 = pygame.image.load('media/graphics/characters/player/player.png') # on ground
enemy_2 = pygame.image.load('media/graphics/characters/player/player_walk_1.png') # random position
enemy_3 = pygame.image.load('media/graphics/characters/player/player_walk_2.png') # on ground

enemies_list = []

# victory screen (9999)
victory_surf = font_large.render("YOU WIN!", False, (64,64,64))
victory_rect = victory_surf.get_rect(center=(400,200))

# general variables
# score
score = 0
high_score = 0

enemy_timer = pygame.USEREVENT+1
pygame.time.set_timer(enemy_timer,1500)

continue_jump = True
third_enemy = 1

start_time = pygame.time.get_ticks()

first_run = True

# display functions
def display_menu():
    display.fill("blue")
    title = font.render("Dino Game", False, (64,64,64))
    title_rect = title.get_rect(center=(400,200))
    display.blit(title, title_rect)

# def display_controls():
#     print("Displaying instructions")
#     # movement: w, s / up, down arrows / space, mouse left button (jump only)

# def display_death_screen():
#     print("displaying death screen")

def display_score():
    global score
    global high_score
    global is_playing
    
    score_surf = font.render(str(score), False, (64,64,64))
    score_rect = score_surf.get_rect(topright = (775, 25))
    display.blit(score_surf, score_rect)
    score = (pygame.time.get_ticks()-start_time)//100
    if score>9999:
        is_playing=False

    hi_score_surf = font.render("High score: "+str(high_score), False, (64,64,64))
    hi_score_rect = hi_score_surf.get_rect(topleft = (500,25))
    display.blit(hi_score_surf, hi_score_rect)

# player functions
def player_jump():
    global player_grav
    global player_rect

    player_grav+=1
    player_rect.y+=player_grav
    if player_rect.bottom>=GROUND_Y:
        player_rect.bottom=GROUND_Y

# def player_crouching():
#     global player_rect
#     global player_crouched

#     player_rect = player_crouched.get_rect(bottomleft = (50,300))

# enemy functions
def enemy_movement(enemies_list):
    global platform_speed

    if enemies_list:
        for enemy in enemies_list:
            enemy.x-=platform_speed

            if enemy.bottom == GROUND_Y-1:
                display.blit(enemy_3, enemy)
            elif enemy.bottom==GROUND_Y:
                display.blit(enemy_1, enemy)
            else:
                display.blit(enemy_2, enemy)
        enemies_list = [enemy for enemy in enemies_list if enemy.right>=0]
        return enemies_list
    else: return []

# collision
def check_collision(player, enemies):

    if enemies:
        for enemy in enemies:
            if player.colliderect(enemy):
                return False
    return True


# main loop
while is_running:
    # check inputs
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_playing = False
            is_running = False
        if is_playing:
            if e.type == enemy_timer:
                third_enemy = random.randint(0,5)
                # print(third_enemy)
                if third_enemy==0:
                        enemies_list.append(enemy_3.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y-1)))
                elif random.randint(0,1):
                    enemies_list.append(enemy_1.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y)))
                elif third_enemy==1 or third_enemy==2 or third_enemy==3:
                        # print("spawned midair")
                        enemies_list.append(enemy_2.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y-100)))
                elif third_enemy==4 or third_enemy==5:
                        # print("spawned near ground")
                        enemies_list.append(enemy_2.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y-30)))
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button==1 and player_rect.bottom==GROUND_Y:
                    player_grav=PLAYER_DEF_GRAV
            if e.type == pygame.KEYDOWN:
                if (e.key==pygame.K_UP or e.key==pygame.K_w or e.key==pygame.K_SPACE) and player_rect.bottom==GROUND_Y:
                    player_grav = PLAYER_DEF_GRAV
                    continue_jump=True
            if e.type == pygame.KEYUP:
                continue_jump=False
        else:
            if e.type == pygame.KEYDOWN and e.key==pygame.K_SPACE:
                is_playing = True
            
                # rects
                background_rect_1.bottomleft=(0,400)
                platform_rect_1.bottomleft=(0, 400)
                player_rect.bottomleft = (50, GROUND_Y)
                enemies_list=[]

                # speeds
                background_speed = DEFAULT_BACKGROUND_SPEED
                platform_speed = DEFAULT_PLATFORM_SPEED

                # score
                if score>high_score and score!=100000:
                    high_score=score
                elif score==10000:
                    high_score=9999
                start_time = pygame.time.get_ticks()
    
    if is_playing:
        # if first_run:
        #     display_menu()

        # background
        background_rect_1.left-=background_speed
        background_rect_2.left-=background_speed
        
        if background_rect_1.right<=800:
            background_rect_2.left=background_rect_1.right
        if background_rect_2.right<=800:
            background_rect_1.left=background_rect_2.right
        
        display.blit(background,background_rect_1)
        display.blit(background,background_rect_2)
        
        # platform
        platform_rect_1.left-=platform_speed
        platform_rect_2.left-=platform_speed

        if platform_rect_1.right<=800:
            platform_rect_2.left=platform_rect_1.right
        if platform_rect_2.right<=800:
            platform_rect_1.left=platform_rect_2.right
        
        display.blit(platform,platform_rect_1)
        display.blit(platform,platform_rect_2)

        # player
        player_jump()
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            # player_crouching()
            print("crouching")
        if key[pygame.K_SPACE] or key[pygame.K_w] or mouse==(True, False, False):
            if player_grav<=0 and player_grav>PLAYER_MAX_GRAV-player_grav and player_rect.y>90 and continue_jump:
                player_grav-=2
            if player_rect.bottom==GROUND_Y:
                player_grav=PLAYER_DEF_GRAV
        display.blit(player_surf, player_rect)

        # enemy
        # enemy_1_rect.left-=platform_speed
        # if enemy_1_rect.right<=0: enemy_1_rect.left=800
        # display.blit(enemy_1, enemy_1_rect)
        
        enemies_list = enemy_movement(enemies_list)

        # foreground
        display.blit(foreground, (0, 250))

        is_playing = check_collision(player_rect, enemies_list)

        # score
        display_score()

        # speed update
        if platform_speed<MAX_PLATFORM_SPEED:
            background_speed+=0.003
            platform_speed+=0.003
    elif score>=99999:
        display.blit(victory_surf, victory_rect)
    else:
        display.fill("black")
    
        # update display
    pygame.display.update()

    # ceiling frame rate
    clock.tick(60)

pygame.quit()