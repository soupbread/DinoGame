import pygame
import random

# splatoon
# attack enemy

pygame.init()

is_running = True
is_playing = False

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

player_in = 0
player_jumping = pygame.image.load('media/graphics/characters/player/player_jump.png')

player_crouch = pygame.image.load('media/graphics/characters/player/player_crouch.png')

player_walk = [player_walk_1, player_walk_2, player_walk_1, player_walk_3]

# player_surf = pygame.image.load('media/graphics/characters/player/player.png')
player_surf = player_walk[player_in]
player_rect = player_surf.get_rect(bottomleft=(50, GROUND_Y))

player_grav = 0
PLAYER_MAX_GRAV = -20
PLAYER_DEF_GRAV = -17

# enemies

enemy_1_1 = pygame.image.load('media/graphics/characters/enemies/enemy_1_frame_1.png')
enemy_1_2 = pygame.image.load('media/graphics/characters/enemies/enemy_1_frame_2.png')
enemy_1_in = 0
enemy_1_frames = [enemy_1_1, enemy_1_2]

enemy_2_1 = pygame.image.load('media/graphics/characters/enemies/enemy_2_frame_1.png')
enemy_2_2 = pygame.image.load('media/graphics/characters/enemies/enemy_2_frame_2.png')
enemy_2_in = 0
enemy_2_frames = [enemy_2_1, enemy_2_2]

enemy_3_1 = pygame.image.load('media/graphics/characters/enemies/enemy_3_frame_1.png')
enemy_3_2 = pygame.image.load('media/graphics/characters/enemies/enemy_3_frame_2.png')
enemy_3_in = 0
enemy_3_frames = [enemy_3_1, enemy_3_2]

enemies_list = []

# victory screen (9999)
victory_surf = font_large.render("YOU WIN!", False, (64,64,64))
victory_rect = victory_surf.get_rect(center=(400,200))

# general variables
# score
score = 0
high_score = 0

enemy_timer = pygame.USEREVENT+1
pygame.time.set_timer(enemy_timer,1200)

continue_jump = True
third_enemy = 1

start_time = pygame.time.get_ticks()
enemy_1_anim = pygame.USEREVENT+2
pygame.time.set_timer(enemy_1_anim, 500)

enemy_2_anim = pygame.USEREVENT+3
pygame.time.set_timer(enemy_2_anim, 200)

enemy_3_anim = pygame.USEREVENT+4
pygame.time.set_timer(enemy_3_anim, 500)

show_menu = True
show_leaderboard = False

text_box_active = False

name = ""

button_surf = pygame.image.load('media/graphics/characters/player/player_crouch.png')
button_rect = button_surf.get_rect(center=(400,300))

text_box_surf = pygame.image.load('media\graphics\characters\player\player.png')
text_box_rect = text_box_surf.get_rect(center=(400,200))

leaderboard_button_surf = pygame.image.load('media\graphics\characters\player\player_crouch.png')
leaderboard_button_rect = leaderboard_button_surf.get_rect(center=(600,200))

line_y = 25

jumping = False

leaderboard_title_surf = font.render('Leaderboard', False, (64,64,64))
leaderboard_title_rect = leaderboard_title_surf.get_rect(center=(200,line_y))

to_m_button_surf = pygame.image.load('media\graphics\characters\player\player_crouch.png')
to_m_button_rect = to_m_button_surf.get_rect(center=(400,350))

# display functions
def display_menu():
    global line_y
    line_y+=10
    title = font.render("Dino Game", True, (22, 36, 16))
    title_rect = title.get_rect(center=(400,100))
    display.fill("seagreen4")
    display.blit(title, title_rect)
    display.blit(button_surf, button_rect)
    display.blit(text_box_surf,text_box_rect)
    
    text_box = font.render(name, True, (22, 0, 16))
    text_rect = text_box.get_rect(topleft=(175,200))
    display.blit(text_box, text_rect)
    
    display.blit(leaderboard_button_surf, leaderboard_button_rect)

def display_leaderboard():
    global line_y

    line_y = 25

    display.fill("seagreen4")
    display.blit(to_m_button_surf,to_m_button_rect)
    display.blit(leaderboard_title_surf, leaderboard_title_rect)
    
    with open('all_player_data/top-10.txt', 'r') as f:
        line_y=60
        for line in f:
            line_y+=20
            line = line.rstrip('\n')
            user_surf = font.render(line, True, (0,0,0))
            user_rect = user_surf.get_rect(topleft=(300,line_y))
            display.blit(user_surf, user_rect)

def display_death_screen():
    global menu_button_rect, file

    display.fill("seagreen4")
    died_surf = font.render("You died! Press space to restart", True, (0,0,0))
    died_rect = died_surf.get_rect(center=(400,200))
    menu_button_surf = pygame.image.load('media\graphics\characters\player\player_walk_3.png')
    menu_button_rect = menu_button_surf.get_rect(center=(400,300))
    display.blit(died_surf, died_rect)
    display.blit(menu_button_surf, menu_button_rect)

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

def get_score(line):
    return int(line.split(',')[0])

def display_tutorial():
    print("hihi")

# player functions
def player_jump():
    global player_grav, player_rect, jumping
    
    player_grav+=1
    player_rect.y+=player_grav
    if player_rect.bottom>=GROUND_Y:
        jumping = False
        player_rect.bottom=GROUND_Y

def player_animation():
    global player_surf, player_in
    
    if player_rect.bottom<GROUND_Y:
       player_surf = player_jumping
    else:
        player_in += 0.2
        if int(player_in) >= len(player_walk):
            player_in=0
        player_surf = player_walk[(int(player_in))]

# no more than 5% of code longer than 80 columns

def player_crouching():
    global player_rect, player_surf, player_grav

    if player_rect.bottom<300:
        player_grav+=4
    else:
        player_surf = player_crouch
        player_rect = player_surf.get_rect(bottomleft = (50, GROUND_Y))

# enemy functions
def enemy_movement(enemies_list):
    global platform_speed

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

    if enemies:
        for enemy in enemies:
            if player.colliderect(enemy):
                return False
    return True

def refresh():
    global background_rect_1, platform_rect_1, player_rect
    global enemies_list, background_speed, platform_speed
    global score, high_score, name

    # rects
    background_rect_1.bottomleft=(0,400)
    platform_rect_1.bottomleft=(0, 400)
    player_rect.bottomleft = (50, GROUND_Y)
    enemies_list=[]

    # speeds
    background_speed = DEFAULT_BACKGROUND_SPEED
    platform_speed = DEFAULT_PLATFORM_SPEED

    # write score
    if score==10000:
        high_score=9999
    elif score>high_score:
        high_score=score

    supp = "0"
    
    with open('all_player_data\leaderboard.txt', 'r') as f:
        all_data = f.read()
    if name in all_data:
        ind = all_data.find(name)
        if high_score>int(all_data[ind-6:ind-2]):
            all_data = all_data.replace(all_data[ind-6:ind-2], supp*(4-len(str(high_score)))+str(high_score))
            with open('all_player_data\leaderboard.txt', 'w') as f:
                f.write(all_data)
    else:
        with open('all_player_data\leaderboard.txt', 'a') as f:
            f.write(supp*(4-len(str(high_score)))+f"{high_score}, {name}\n")
    with open('all_player_data\leaderboard.txt', 'r') as f:
        lines = f.readlines()
    lines.sort(key=get_score, reverse=True)
    with open('all_player_data\leaderboard.txt', 'w') as f:
        f.writelines(lines)
    with open('all_player_data\\top-10.txt', 'w') as f:
        f.writelines(lines[:10])

# main loop
while is_running:
    # check inputs

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_playing = False
            is_running = False
        if is_playing:
            if e.type == enemy_timer:
                third_enemy = random.randint(0,5)
                # print(third_enemy)
                if third_enemy==0:
                        enemies_list.append(enemy_3.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y+1)))
                elif random.randint(0,1):
                    enemies_list.append(enemy_1.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y)))
                elif third_enemy==1 or third_enemy==2 or third_enemy==3:
                        # print("spawned midair")
                        enemies_list.append(enemy_2.get_rect(bottomleft=(random.randint(1000, 1200), GROUND_Y-100)))
                elif third_enemy==4 or third_enemy==5:
                        # print("spawned near ground")
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
                if (e.key==pygame.K_UP or e.key==pygame.K_w or e.key==pygame.K_SPACE) and player_rect.bottom==GROUND_Y:
                    player_grav = PLAYER_DEF_GRAV
                    continue_jump=True
            if e.type == pygame.KEYUP:
                continue_jump=False
        else:
            if e.type == pygame.MOUSEBUTTONUP:
                if show_menu:
                    if button_rect.collidepoint(mouse_x, mouse_y) and show_menu and not show_leaderboard:
                        with open('all_player_data/leaderboard.txt', 'r') as f:
                            all_data = f.read()
                        if name=="":
                            name = "Guest"
                        if name in all_data:
                            ind = all_data.find(name)
                            high_score = int(all_data[ind-6:ind-2])
                        print("start game")
                        is_playing=True
                    if text_box_rect.collidepoint(mouse_x, mouse_y) and not text_box_active:
                        print("text box activated")
                        text_box_active = True
                    if not text_box_rect.collidepoint(mouse_x, mouse_y) and text_box_active:
                        print("text box deactivated")
                        text_box_active = False
                    if leaderboard_button_rect.collidepoint(mouse_x, mouse_y) and show_menu:
                        print('display leaderboard')
                        show_leaderboard=True
                    if show_leaderboard and to_m_button_rect.collidepoint(mouse_x, mouse_y):
                        print('leaderboard closed')
                        show_leaderboard=False
                else:
                    if menu_button_rect.collidepoint(mouse_x, mouse_y):
                        print("return to menu")
                        refresh()
                        show_menu = True
            if e.type == pygame.KEYDOWN:
                if text_box_active == True:
                    if e.key == pygame.K_RETURN:
                        text_box_active = False
                        print("text box deactivated")
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name+=e.unicode
                elif e.key==pygame.K_SPACE and not show_menu:
                    is_playing = True
                    refresh()
                    start_time = pygame.time.get_ticks()

    if is_playing:
        show_menu=False

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
        if key[pygame.K_SPACE] or key[pygame.K_w] or mouse==(True, False, False):
            jumping = True
            if player_grav<=0 and player_grav>PLAYER_MAX_GRAV-player_grav and player_rect.y>90 and continue_jump:
                player_grav-=2
            if player_rect.bottom==GROUND_Y:
                player_grav=PLAYER_DEF_GRAV
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            player_crouching()
        elif not jumping:
            player_rect = player_surf.get_rect(bottomleft=(50,GROUND_Y))
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