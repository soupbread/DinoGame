"""This program uses pygame to run a game similar to the Chrome dino game.
"""

import random

import pygame

__author__ = "Molly Mao"
__copyright__ = "Copyright 2024, Anderson Innovations"
__credits__ = ["Molly Mao"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Molly Mao"
__email__ = "example@example.com"
__status__ = "Production"

pygame.init()

is_running = True
is_playing = False

# window
pygame.display.set_caption("Dino")
pygame.display.set_icon(pygame.image.load('media/dino.png'))

# font
font = pygame.font.Font('media/font/GOUDYSTO.TTF')
font_large = pygame.font.Font("media/font/GOUDYSTO.TTF", 60)

# display
display = pygame.display.set_mode((800,400))

# background
background = pygame.image.load(
    'media/graphics/environment/sky.png').convert()
background_rect_1 = background.get_rect(bottomleft=(0,400))
background_rect_2 = background.get_rect(
    bottomleft=background_rect_1.bottomright)

DEFAULT_BACKGROUND_SPEED = 4
background_speed = DEFAULT_BACKGROUND_SPEED

# platform
platform = pygame.image.load('media/graphics/environment/ground.png').convert()
platform_rect_1 = platform.get_rect(bottomleft=(0,400))
platform_rect_2 = platform.get_rect(bottomleft=platform_rect_1.bottomright)

DEFAULT_PLATFORM_SPEED = 6
MAX_PLATFORM_SPEED = 20
platform_speed = DEFAULT_PLATFORM_SPEED

GROUND_Y = 300

# foreground
foreground = pygame.image.load(
    'media/graphics/environment/foreground.png').convert_alpha()

# apple
apple_surf = pygame.image.load('media/graphics/apple.png').convert_alpha()
apple_rect = apple_surf.get_rect(bottomleft=(800,GROUND_Y))
apple_list = []

# player
player_walk_1 = pygame.image.load(
    'media/graphics/characters/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load(
    'media/graphics/characters/player/player_walk_2.png').convert_alpha()
player_walk_3 = pygame.image.load(
    'media/graphics/characters/player/player_walk_3.png').convert_alpha()

player_walk_1_god = pygame.image.load(
    'media/graphics/characters/player/player_walk_1 - god.png').convert_alpha()
player_walk_2_god = pygame.image.load(
    'media/graphics/characters/player/player_walk_2 - god.png').convert_alpha()
player_walk_3_god = pygame.image.load(
    'media/graphics/characters/player/player_walk_3 - god.png').convert_alpha()

player_in = 0
player_jumping = pygame.image.load(
    'media/graphics/characters/player/player_jump.png').convert_alpha()
player_jumping_god = pygame.image.load(
    'media/graphics/characters/player/player_jump - god.png').convert_alpha()

player_crouch = pygame.image.load(
    'media/graphics/characters/player/player_crouch.png').convert_alpha()
player_crouch_god = pygame.image.load(
    'media/graphics/characters/player/player_crouch - god.png').convert_alpha()

player_walk = [player_walk_1, player_walk_2, player_walk_1, player_walk_3]
player_walk_god = [
    player_walk_1_god, player_walk_2_god, player_walk_1_god, player_walk_3_god]

player_surf = player_walk[player_in]
player_rect = player_surf.get_rect(bottomleft=(50, GROUND_Y))

player_grav = 0
PLAYER_MAX_GRAV = -20
PLAYER_DEF_GRAV = -17

# player info / status
score = 0
high_score = 0

name = ""

continue_jump = True
jumping = False

god_mode = False

# enemies
enemy_1_1 = pygame.image.load(
    'media/graphics/characters/enemies/enemy_1_frame_1.png').convert_alpha()
enemy_1_2 = pygame.image.load(
    'media/graphics/characters/enemies/enemy_1_frame_2.png').convert_alpha()
enemy_1_in = 0
enemy_1_frames = [enemy_1_1, enemy_1_2]
enemy_1 = enemy_1_frames[0]

enemy_2_1 = pygame.image.load(
    'media/graphics/characters/enemies/enemy_2_frame_1.png').convert_alpha()
enemy_2_2 = pygame.image.load(
    'media/graphics/characters/enemies/enemy_2_frame_2.png').convert_alpha()
enemy_2_in = 0
enemy_2_frames = [enemy_2_1, enemy_2_2]
enemy_2 = enemy_2_frames[0]

enemy_3_1 = pygame.image.load(
    'media/graphics/characters/enemies/enemy_3_frame_1.png').convert_alpha()
enemy_3_2 = pygame.image.load(
    'media/graphics/characters/enemies/enemy_3_frame_2.png').convert_alpha()
enemy_3_in = 0
enemy_3_frames = [enemy_3_1, enemy_3_2]
enemy_3 = enemy_3_frames[0]

third_enemy = 1

enemies_list = []

# victory
victory_surf = font_large.render("YOU WIN!", False, (64,64,64))
victory_rect = victory_surf.get_rect(center=(400,200))

# menu
title = font_large.render("Dino Game", True, (22, 36, 16))
title_rect = title.get_rect(center=(400,100))

start_button_surf = font.render('Start', True, (64,64,64))
start_button_rect = start_button_surf.get_rect(center=(400,300))

text_box_surf = pygame.image.load('media/graphics/text_box.png').convert()
text_box_rect = text_box_surf.get_rect(center=(500,235))

leaderboard_button_surf = font.render('Leaderboard', True, (64,64,64))
leaderboard_button_rect = leaderboard_button_surf.get_rect(center=(400,175))

name_text = font.render("Player:", True, (22, 0, 16))

# leaderboard

leaderboard_title_surf = font.render('Leaderboard', False, (64,64,64))
leaderboard_title_rect = leaderboard_title_surf.get_rect(center=(200,25))

# death
died_surf = font.render("You died! Press space to restart", True, (0,0,0))
died_rect = died_surf.get_rect(center=(400,100))

menu_button_surf = font.render("Return to Menu", True, (64,64,64))
menu_button_rect = menu_button_surf.get_rect(center=(400,350))

# clocks
clock = pygame.time.Clock()
start_time = 0

enemy_timer = pygame.USEREVENT+1
pygame.time.set_timer(enemy_timer,1200)

start_time = pygame.time.get_ticks()
enemy_1_anim = pygame.USEREVENT+2
pygame.time.set_timer(enemy_1_anim, 500)

enemy_2_anim = pygame.USEREVENT+3
pygame.time.set_timer(enemy_2_anim, 200)

enemy_3_anim = pygame.USEREVENT+4
pygame.time.set_timer(enemy_3_anim, 500)

apple_timer = pygame.USEREVENT+5
pygame.time.set_timer(apple_timer, random.randint(20000, 30000))

god_mode_timer = pygame.USEREVENT+6 

# display bools
show_menu = True
show_leaderboard = False
text_box_active = False
victory = False

# display functions
def display_menu():
    """Displays the main menu.
    """
    display.fill("seagreen4")
    display.blit(title, title_rect)
    display.blit(start_button_surf, start_button_rect)
    display.blit(text_box_surf,text_box_rect)
    
    text_box = font.render(name, True, (22, 0, 16))
    text_rect = text_box.get_rect(center=(500,235))
    display.blit(text_box, text_rect)
    
    display.blit(name_text, name_text.get_rect(center=(325, 235)))
    display.blit(leaderboard_button_surf, leaderboard_button_rect)

def display_leaderboard():
    """Displays the leadeboard screen.
    """
    display.fill("seagreen4")
    display.blit(menu_button_surf,menu_button_rect)
    display.blit(leaderboard_title_surf, leaderboard_title_rect)
    
    with open('all_player_data/top-10.txt', 'r') as f:
        line_y=60
        place = 0
        for line in f:
            line_y+=20
            place+=1
            line = line.rstrip('\n')
            user_surf = font.render(f"{place}. {line}", True, (0,0,0))
            user_rect = user_surf.get_rect(topleft=(300,line_y))
            display.blit(user_surf, user_rect)

def display_death_screen():
    """Displays the game over screen.
    """
    global menu_button_rect

    display.fill("seagreen4")
    player_surf = pygame.transform.scale2x(player_crouch)
    display.blit(player_surf, player_surf.get_rect(center=(400,200)))
    display.blit(died_surf, died_rect)
    display.blit(menu_button_surf, menu_button_rect)

def display_victory_screen():
    """Displays the victory screen.
    """
    display.blit(victory_surf, victory_rect)
    display.blit(menu_button_surf, menu_button_rect)

def display_score():
    """Displays the score and high score on the game screen.
    """
    global score, high_score, is_playing, victory
    
    score_surf = font.render(str(score), False, (64,64,64))
    score_rect = score_surf.get_rect(topright = (775, 25))
    display.blit(score_surf, score_rect)
    score = (pygame.time.get_ticks()-start_time)//100
    if score>9999:
        is_playing=False
        victory = True

    hi_score_surf = font.render(
        "High score: "+str(high_score), False, (64,64,64))
    hi_score_rect = hi_score_surf.get_rect(topleft = (500,25))
    display.blit(hi_score_surf, hi_score_rect)

def get_score(line):
    """Reads a line in the leaderboard.txt file and extracts the score from it.

    Args:
        line String: a line in the leaderboard.txt file

    Returns:
        int: the score of the user
    """
    return int(line.split(',')[0])

# player functions
def player_jump():
    """Changes the y position of the player rectangle to jump.
    """
    global player_grav, player_rect, jumping
    
    player_grav+=1
    player_rect.y+=player_grav
    if player_rect.bottom>=GROUND_Y:
        jumping = False
        player_rect.bottom=GROUND_Y

def player_animation():
    """Animates the player (not including crouch).
    """
    global player_surf, player_in
    
    if player_rect.bottom<GROUND_Y:
        if not god_mode:
           player_surf = player_jumping
        else:
           player_surf = player_jumping_god
    
    else:
        player_in += 0.2
        if int(player_in) >= len(player_walk):
            player_in=0
        if not god_mode:
            player_surf = player_walk[(int(player_in))]
        else:
            player_surf = player_walk_god[(int(player_in))]

def player_crouching():
    """Allows the player to crouch.

    Changes the player sprite to a crouching sprite.
    If the player is in the air, the gravity is increased when crouching
    to allow the player to drop back onto the ground sooner.
    """
    global player_rect, player_surf, player_grav

    if player_rect.bottom<300:
        player_grav+=4
    else:
        if not god_mode:
            player_surf = player_crouch
        else:
            player_surf = player_crouch_god
        player_rect = player_surf.get_rect(bottomleft = (50, GROUND_Y))

# apple functions
def apple_movement(applelist):
    """Moves the apple rect that enables god mode.

    Moves each apple rect in the list across the screen.
    If an apple is off the screen or if god mode is achieved
    (meaning the apple has been eaten), then all apples
    are removed from the list.
    
    Args:
        applelist (list): List of all apple rects on the screen.

    Returns:
        list: An updated list of apple rects on the screen.
    """
    if not god_mode:
        if applelist:
            for apple in applelist:
                apple.x-=platform_speed
                display.blit(apple_surf, apple)
            applelist = [apple for apple in applelist if apple.right>=0]
            return applelist
        else: return []
    else: return []

def apple_collision(player, apples):
    """Checks if apple collides with the player.

    Args:
        player (pygame.rect.Rect): the player rect
        apples (list): the list of apple rects on the screen

    Returns:
        boolean: whether or not the player has collided with an apple rect
    """
    if not god_mode:
        if apples:
            for apple in apples:
                if player.colliderect(apple):
                    pygame.time.set_timer(god_mode_timer, (10000))
                    return True
    return False

# enemy functions
def enemy_movement(enemies_list):
    """Moves the enemy rects.

    Moves each enemy rect in the list across the screen.
    If an enemy rect is off the screen, then it is removed
    from the list. If there are no elements in the list,
    then an empty list is returned.
    
    Args:
        enemies_list (list): List of all enemy rects on the screen.

    Returns:
        list: An updated list of enemy rects on the screen.
    """
    if enemies_list:
        for enemy in enemies_list:
            enemy.x-=platform_speed

            if enemy.bottom == GROUND_Y+1:
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
    """Checks if the player rect has collided with an enemy rect.

    If god mode is activated, collisions are not checked for.

    Args:
        player (pygame.rect.Rect): the player rect
        enemies (list): the list of enemy rects

    Returns:
        boolean: whether or not the player rect has collided with an enemy rect
    """
    if not god_mode:
        if enemies:
            for enemy in enemies:
                if player.colliderect(enemy):
                    return False
    return True

def refresh_placement():
    """Resets sprites to their original location. Clears enemies and apples. 
    Resets timers. Resets the speed.
    """
    global background_rect_1, platform_rect_1, player_rect
    global enemies_list, background_speed, platform_speed
    global apple_list, god_mode

    # rects
    background_rect_1.bottomleft=(0,400)
    platform_rect_1.bottomleft=(0, 400)
    player_rect.bottomleft = (50, GROUND_Y)
    enemies_list=[]
    apple_list=[]

    # speeds
    background_speed = DEFAULT_BACKGROUND_SPEED
    platform_speed = DEFAULT_PLATFORM_SPEED

def reset_timers():
    """Resets all timers.
    """
    # timers
    pygame.time.set_timer(enemy_timer,1200)
    pygame.time.set_timer(enemy_1_anim, 500)
    pygame.time.set_timer(enemy_2_anim, 200)
    pygame.time.set_timer(enemy_3_anim, 500)
    pygame.time.set_timer(apple_timer, random.randint(20000, 30000))

def update_high_score():
    """Sets player high score to current score if current score is higher
    """
    global score, high_score

    if score==10000:
        high_score=9999
    elif score>high_score:
        high_score=score

def write_data():
    """Writes player name and score to leaderboard files.

    Reads leaderboard.txt and saves it as a String in the all_data variable.
    Checks if this user has played before.
    If so, update the user's high score if it has been exceeded.
    Otherwise, add the user's name and score to a new line.
    Sort the leaderboard by score.
    """
    with open('all_player_data/leaderboard.txt', 'r') as f:
        all_data = f.read()
    if name in all_data:
        ind = all_data.find(name)
        if high_score>int(all_data[ind-6:ind-2]):
            all_data = all_data.replace(all_data[ind-6:ind-2], "0"*(4-len(str(high_score)))+str(high_score))
            with open('all_player_data/leaderboard.txt', 'w') as f:
                f.write(all_data)
    else:
        with open('all_player_data/leaderboard.txt', 'a') as f:
            f.write("0"*(4-len(str(high_score)))+f"{high_score}, {name}\n")
    with open('all_player_data/leaderboard.txt', 'r') as f:
        all_data = f.readlines()
    all_data.sort(key=get_score, reverse=True)
    with open('all_player_data/leaderboard.txt', 'w') as f:
        f.writelines(all_data)
    with open('all_player_data/top-10.txt', 'w') as f:
        f.writelines(all_data[:10])

# main loop
while is_running:
    # check inputs

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_playing = False
            is_running = False
        if is_playing:
            if e.type == god_mode_timer and god_mode:
                god_mode = False
                pygame.time.set_timer(apple_timer, random.randint(20000, 30000))
            if e.type == apple_timer:
                apple_list.append(apple_surf.get_rect(bottomleft=(900,GROUND_Y)))
            if e.type == enemy_timer:
                third_enemy = random.randint(0,5)
                if third_enemy==0:
                        enemies_list.append(enemy_3.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y+1)))
                elif random.randint(0,1):
                    enemies_list.append(enemy_1.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y)))
                elif third_enemy==1 or third_enemy==2 or third_enemy==3:
                        enemies_list.append(enemy_2.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y-100)))
                elif third_enemy==4 or third_enemy==5:
                        enemies_list.append(enemy_2.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y-60)))
            if e.type == enemy_1_anim:
                if enemy_1_in==0: enemy_1_in=1
                else: enemy_1_in = 0
                enemy_1 = enemy_1_frames[enemy_1_in]
            if e.type == enemy_2_anim:
                if enemy_2_in==0: enemy_2_in=1
                else: enemy_2_in = 0
                enemy_2 = enemy_2_frames[enemy_2_in]
            if e.type == enemy_3_anim:
                if enemy_3_in==0: enemy_3_in=1
                else: enemy_3_in = 0
                enemy_3 = enemy_3_frames[enemy_3_in]
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button==1 and player_rect.bottom==GROUND_Y:
                    player_grav=PLAYER_DEF_GRAV
                    continue_jump=True
            if e.type == pygame.KEYDOWN:
                if (e.key==pygame.K_UP or
                    e.key==pygame.K_w or
                    e.key==pygame.K_SPACE
                    and player_rect.bottom==GROUND_Y):
                    player_grav = PLAYER_DEF_GRAV
                    continue_jump=True
            if e.type == pygame.KEYUP:
                continue_jump=False
        else:
            if e.type == pygame.MOUSEBUTTONUP:
                if show_menu:
                    if not show_leaderboard:
                        if (
                        start_button_rect.collidepoint(mouse_x, mouse_y) 
                        and show_menu 
                        and not victory
                        ):
                            with open('all_player_data/leaderboard.txt', 'r') as f:
                                all_data = f.read()
                            if name=="":
                                name = "Guest"
                            if name in all_data:
                                ind = all_data.find(name)
                                high_score = int(all_data[ind-6:ind-2])
                            else:
                                high_score = 0
                            refresh_placement()
                            reset_timers()
                            god_mode = False
                            is_playing=True
                        if (text_box_rect.collidepoint(mouse_x, mouse_y) and 
                            not text_box_active):
                            text_box_active = True
                        if (
                            not text_box_rect.collidepoint(mouse_x, mouse_y)
                            and text_box_active):
                            text_box_active = False
                        if leaderboard_button_rect.collidepoint(
                            mouse_x, mouse_y) and show_menu:
                            show_leaderboard=True
                    elif menu_button_rect.collidepoint(mouse_x, mouse_y):
                        show_leaderboard=False
                elif menu_button_rect.collidepoint(mouse_x, mouse_y):
                        show_menu = True
                        update_high_score()
                        write_data()
            if e.type == pygame.KEYDOWN:
                if text_box_active == True:
                    if e.key == pygame.K_RETURN:
                        text_box_active = False
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name+=e.unicode
                elif e.key==pygame.K_SPACE and not show_menu:
                    is_playing = True
                    refresh_placement()
                    update_high_score()
                    write_data()
                    god_mode = False
                    reset_timers()
                    start_time = pygame.time.get_ticks()

    if is_playing:
        show_menu=False
        victory = False

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
        player_animation()
        if (
            key[pygame.K_SPACE] or 
            key[pygame.K_w] or 
            mouse==(True, False, False)
            ):
            jumping = True
            if (
                player_grav<=0 and 
                player_grav>PLAYER_MAX_GRAV-player_grav and # puts a cap on the jump height
                player_rect.y>90 and 
                continue_jump
                ):
                player_grav-=2
            if player_rect.bottom==GROUND_Y:
                player_grav=PLAYER_DEF_GRAV
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            player_crouching()
        elif not jumping:
            player_rect = player_surf.get_rect(bottomleft=(50,GROUND_Y))
        
        if not god_mode:
            god_mode = apple_collision(player_rect, apple_list)
        
        display.blit(player_surf, player_rect)
        
        enemies_list = enemy_movement(enemies_list)
        apple_list = apple_movement(apple_list)

        # foreground
        display.blit(foreground, (0, 250))

        # score
        display_score()

        is_playing = check_collision(player_rect, enemies_list)

        # speed update
        if platform_speed<MAX_PLATFORM_SPEED:
            background_speed+=0.003
            platform_speed+=0.003

    elif victory:
        display_victory_screen()
    elif show_menu and show_leaderboard:
        display_leaderboard()
    elif show_menu:
        display_menu()
        start_time = pygame.time.get_ticks()
    else:
        display_death_screen()
    
    # update display
    pygame.display.update()

    # ceiling frame rate
    clock.tick(60)

pygame.quit()