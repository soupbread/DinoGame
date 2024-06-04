import pygame

pygame.init()

is_running = True
is_playing = True

# window
pygame.display.set_caption("Dino")
pygame.display.set_icon(pygame.image.load('media/dino.png'))

# font
font = pygame.font.Font('media/font/GOUDYSTO.TTF')

# time
clock = pygame.time.Clock()
start_time = 0

# display
display = pygame.display.set_mode((800,400))

# background
background = pygame.image.load('media/graphics/environment/sky.png')
background_rect_1 = background.get_rect(bottomleft=(0,400))
background_rect_2 = background.get_rect(bottomleft=background_rect_1.bottomright)

DEFAULT_BACKGROUND_SPEED = 2
background_speed = 2

# platform
platform = pygame.image.load('media/graphics/environment/ground.png')
platform_rect_1 = platform.get_rect(bottomleft=(0,400))
platform_rect_2 = platform.get_rect(bottomleft=platform_rect_1.bottomright)

DEFAULT_PLATFORM_SPEED = 5
platform_speed = 5

# foreground
foreground = pygame.image.load('media/graphics/environment/foreground.png')

# player
player = pygame.image.load('media/graphics/characters/player/player.png')
player_rect = player.get_rect(bottomleft=(50, 300))

player_grav = 0

# enemies
enemy_1 = pygame.image.load('media/graphics/characters/player/player.png')
enemy_1_rect = enemy_1.get_rect(bottomleft=(800, 300))

# general variables
# score
score = 0
high_score = 0

start_time = pygame.time.get_ticks()

# display functions
def display_menu():
    print("Displaying title screen")

def display_controls():
    print("Displaying instructions")
    # movement: w, s / up, down arrows / space, mouse left button (jump only)

def display_death_screen():
    print("displaying death screen")

def display_score():
    global score
    global high_score

    score = pygame.time.get_ticks()-start_time
    score_surf = font.render(str(score), False, (64,64,64))
    score_rect = score_surf.get_rect(topright = (775, 25))
    display.blit(score_surf, score_rect)

    hi_score_surf = font.render("High score: "+str(high_score), False, (64,64,64))
    hi_score_rect = hi_score_surf.get_rect(topleft = (500,25))
    display.blit(hi_score_surf, hi_score_rect)

# player functions
def player_jump():
    global player_grav
    global player_rect

    player_grav+=1
    player_rect.y+=player_grav
    if player_rect.bottom>=300:
        player_rect.bottom=300

def player_crouch():
    print("CROUCHING")

# main loop
while is_running:
    # check inputs
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_playing = False
            is_running = False
        if is_playing:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button==1 and player_rect.bottom==300:
                    player_grav=-20
            if e.type == pygame.KEYDOWN:
                if (e.key==pygame.K_UP or e.key==pygame.K_w or e.key==pygame.K_SPACE) and player_rect.bottom==300:
                    player_grav = -20
                if e.key==pygame.K_DOWN or e.key==pygame.K_s:
                    # player_crouch()
                    pass
        else:
            if e.type == pygame.KEYDOWN and e.key==pygame.K_SPACE:
                is_playing = True
            
                # rects
                background_rect_1.bottomleft=(0,400)
                platform_rect_1.bottomleft=(0, 400)
                enemy_1_rect.bottomleft=(800,300)

                # speeds
                background_speed = DEFAULT_BACKGROUND_SPEED
                platform_speed = DEFAULT_PLATFORM_SPEED

                # score
                if score>high_score:
                    high_score=score
                print("hi",high_score)
                start_time = pygame.time.get_ticks()
    if is_playing:
        # update start time

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
        # player_crouch()
        display.blit(player, player_rect)

        # enemy
        enemy_1_rect.left-=platform_speed
        if enemy_1_rect.right<=0: enemy_1_rect.left=800
        display.blit(enemy_1, enemy_1_rect)

        # foreground
        display.blit(foreground, (0, 250))

        # score
        display_score()

        # collision
        if enemy_1_rect.colliderect(player_rect):
            print("you died")
            # display.fill("black")
            # display_death_screen()
            is_playing = False
        
        # speed update
        background_speed+=0.0001
        platform_speed+=0.0001

        # update display
        pygame.display.update()

        # ceiling frame rate
        clock.tick(60)

pygame.quit()