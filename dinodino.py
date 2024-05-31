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

# other
collision_cnt=0

while is_running:
    # check whether window has been closed
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    # surfaces
    display.blit(background, (0,0))
    display.blit(ground, ground_rect_1)
    display.blit(ground, ground_rect_2)
    display.blit(player, player_rect)

    display.blit(test_enemy, test_enemy_rect)
    test_enemy_rect.left-=5
    if test_enemy_rect.right<=0: test_enemy_rect.left=800

    display.blit(foreground, (0, 250))

    # infinite scrolling
    ground_rect_1.left-=5
    ground_rect_2.left-=5

    if ground_rect_1.right<=800: ground_rect_2.left=ground_rect_1.right
    if ground_rect_2.right<=800: ground_rect_1.left=ground_rect_2.right

    if test_enemy_rect.colliderect(player_rect): collision_cnt+=1
    else: collision_cnt=0

    if collision_cnt==1: print("COLLISION")

    # update display
    pygame.display.update()

    # ceiling frame rate
    clock.tick(60)