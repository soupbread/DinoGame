import pygame

pygame.init()

is_running = True
is_playing = True

# window properties
pygame.display.set_caption("Dino")
pygame.display.set_icon(pygame.image.load('media/dino.png'))

# display (screen)
display = pygame.display.set_mode((800,400))

# clock
clock = pygame.time.Clock()

# surfaces
background = pygame.image.load('media/graphics/environment/sky.png')

ground = pygame.image.load('media/graphics/environment/ground.png')
ground_rect_1 = ground.get_rect(bottomleft=(0,400))
ground_rect_2 = ground.get_rect(bottomleft=ground_rect_1.bottomright)

foreground = pygame.image.load('media/graphics/environment/foreground.png')

# characters
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
speed = 5

died = pygame.image.load('media/cover2.jpg')

# title screen
def title_screen():
    print("Displaying title screen")

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

    test_enemy_rect.bottomleft=(700, 300)
    ground_rect_1.bottomleft=(0,400)
    player_rect.bottomleft=(50, 300)

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
        test_enemy_rect.left-=5
        if test_enemy_rect.right<=0: test_enemy_rect.left=800

        # collision
        if test_enemy_rect.colliderect(player_rect):
            print("you died")
            display.blit(died, (0,0))
            is_playing = False

        # update display
        pygame.display.update()

        # ceiling frame rate
        clock.tick(60)

pygame.quit()