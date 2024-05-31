import pygame

pygame.init()

is_running = True

# window properties
pygame.display.set_caption("Dino")
pygame.display.set_icon(pygame.image.load('media\dino.png'))

# display (screen)
display = pygame.display.set_mode((800,400))

# clock
clock = pygame.time.Clock()

# surfaces
background = pygame.image.load('media\graphics\environment\sky.png')

ground = pygame.image.load('media\graphics\environment\ground.png')
ground_rect_1 = ground.get_rect(bottomleft=(0,400))
ground_rect_2 = ground.get_rect(bottomleft=ground_rect_1.bottomright)

foreground = pygame.image.load('media\graphics\environment\\foreground.png')

# characters
# player
player = pygame.image.load('media\graphics\characters\player\player.png')
player_rect = player.get_rect(bottomleft=(50, 300))

# enemies
test_enemy = pygame.image.load('media\graphics\characters\player\player.png')
test_enemy_rect = test_enemy.get_rect(bottomleft=(700, 300))

# general variables
gravity = 10

# title screen
def title_screen():
    print("Displaying title screen")

while is_running:
    # check whether window has been closed
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            is_running=False
        if e.type == pygame.MOUSEBUTTONDOWN:
            print("mouse pressed")
            if e.button==1:
                print("left mouse button pressed")
        if e.type == pygame.KEYDOWN:
            print("keydown")
            if e.key==pygame.K_UP or e.key==pygame.K_w or e.key==pygame.K_SPACE:
                print("JUMP")
            if e.key==pygame.K_DOWN or e.key==pygame.K_s:
                print("CROUCH")
        if e.type==pygame.KEYUP:
            print("keyup")
    if not is_running:
        break

    # or use exit()

    # surfaces
    display.blit(background, (0,0))
    display.blit(ground, ground_rect_1)
    display.blit(ground, ground_rect_2)
    display.blit(player, player_rect)
    display.blit(test_enemy, test_enemy_rect)
    display.blit(foreground, (0, 250))

    # player movement
    # if pygame.key.get_pressed()[pygame.K_SPACE]:
    #     print("JUMP")

    # enemy movement
    test_enemy_rect.left-=5
    if test_enemy_rect.right<=0: test_enemy_rect.left=800

    # infinite scrolling platform
    ground_rect_1.left-=5
    ground_rect_2.left-=5

    if ground_rect_1.right<=800:
        ground_rect_2.left=ground_rect_1.right
    if ground_rect_2.right<=800:
        ground_rect_1.left=ground_rect_2.right

    # collision
    if test_enemy_rect.colliderect(player_rect): collision_cnt+=1
    else: collision_cnt=0

    if collision_cnt==1: print("COLLISION")

    # update display
    pygame.display.update()

    # ceiling frame rate
    clock.tick(60)