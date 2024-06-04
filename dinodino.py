import pygame

pygame.init()

# status
is_running = True
is_playing = True

test_font = pygame.font.Font('media/font/GOUDYSTO.TTF')

# window properties
pygame.display.set_caption("Dino")
pygame.display.set_icon(pygame.image.load('media/dino.png'))

# display (screen) init
display = pygame.display.set_mode((800,400))

# clock
clock = pygame.time.Clock()

# surfaces
background = pygame.image.load('media/graphics/environment/sky.png')

ground = pygame.image.load('media/graphics/environment/ground.png')
ground_rect_1 = ground.get_rect(bottomleft=(0,400))
ground_rect_2 = ground.get_rect(bottomleft=ground_rect_1.bottomright)

foreground = pygame.image.load('media/graphics/environment/foreground.png')

# player
player = pygame.image.load('media/graphics/characters/player/player.png')
player_rect = player.get_rect(bottomleft=(50, 300))
player_grav = 0

# enemies
test_enemy = pygame.image.load('media/graphics/characters/player/player.png')
test_enemy_rect = test_enemy.get_rect(bottomleft=(700, 300))
# test_enemy_grav = -20

# general variables
score = 0
score_time = 0
high_score = 0
speed = 5
key_pressed_time = 0
start_time = 0
time = 0

# title screen
def title_screen():
    print("Displaying title screen")

def display_score():
    global high_score

    hi_sco_surf = test_font.render(str(high_score), False, (64,64,64))
    hi_sco_rect = hi_sco_surf.get_rect(topleft = (25,25))
    display.blit(hi_sco_surf, hi_sco_rect)
    
    time = pygame.time.get_ticks()-start_time
    score_surface = test_font.render(str(time), False, (64,64,64))
    score_rect = score_surface.get_rect(topright = (775, 25))
    display.blit(score_surface, score_rect)

def player_jump():
    global player_grav
    global player_rect
    
    player_grav+=1
    player_rect.y+=player_grav
    if player_rect.bottom>=300:
        player_rect.bottom=300

def restart():
    global player_rect
    global test_enemy_rect
    global ground_rect_1
    global speed
    global time
    global start_time
    global high_score
    
    if time>high_score:
        high_score = time
    print(high_score)
    print(time)
    test_enemy_rect.bottomleft=(700, 300)
    ground_rect_1.bottomleft=(0,400)
    player_rect.bottomleft=(50, 300)
    speed = 5
    start_time = pygame.time.get_ticks()

while is_running:
    # check whether window has been closed
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_running = False
            is_playing = False
        elif is_playing:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button==1 and player_rect.bottom==300:
                    player_grav=-20
            if e.type == pygame.KEYDOWN:
                if (e.key==pygame.K_UP or e.key==pygame.K_w or e.key==pygame.K_SPACE) and player_rect.bottom==300:
                    player_grav=-20

                if e.key==pygame.K_DOWN or e.key==pygame.K_s:
                    print("CROUCH")
        else:
            if e.type == pygame.KEYDOWN and e.key==pygame.K_SPACE:
                is_playing = True
                restart()
    
    if is_playing:
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if key[pygame.K_SPACE] or key[pygame.K_UP] or mouse==1:
            print("jump key pressed")

        # all surfaces
        display.blit(background, (0,0))
        display.blit(ground, ground_rect_1)
        display.blit(ground, ground_rect_2)
        display.blit(player, player_rect)
        display.blit(test_enemy, test_enemy_rect)
        display.blit(foreground, (0, 250))

        # infinite scrolling platform
        ground_rect_1.left-=speed
        ground_rect_2.left-=speed

        if ground_rect_1.right<=800:
            ground_rect_2.left=ground_rect_1.right
        if ground_rect_2.right<=800:
            ground_rect_1.left=ground_rect_2.right

        # player movement
        player_jump()

        # enemy movement
        test_enemy_rect.left-=speed
        if test_enemy_rect.right<=0: test_enemy_rect.left=800

        # collision
        if test_enemy_rect.colliderect(player_rect):
            print("you died")
            display.fill("black")
            is_playing = False

        speed+=0.0001

        display_score()

        # update display
        pygame.display.update()

        # ceiling frame rate
        clock.tick(60)

pygame.quit()