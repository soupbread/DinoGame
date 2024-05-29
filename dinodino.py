import pygame

game_name = "Dino"
game_icon = pygame.image.load("dino.png")

display_width = 300
display_height = 300

running = True

pygame.init()

pygame.display.set_caption(game_name)
pygame.display.set_icon(game_icon)

screen = pygame.display.set_mode((display_width, display_height))
screen.fill("green")
clock = pygame.time.Clock()

surface = pygame.Surface((display_width-100, display_height-100))
surface.fill("white")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill("green")
    surface.fill("white")
    screen.blit(surface, (50,50))

    pygame.display.update()

    clock.tick(60)