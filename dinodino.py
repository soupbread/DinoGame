import pygame

running = True

pygame.init()

# Display-related init
# Window
game_name = "Dino"
game_icon = pygame.image.load('media\dino.png')

pygame.display.set_caption(game_name)
pygame.display.set_icon(game_icon)

# Font
font = pygame.font.Font('media\\font\GOUDYSTO.TTF', 50)

# Screen
display_width = 1080
display_height = 720

screen = pygame.display.set_mode((display_width, display_height))

# Clock
clock = pygame.time.Clock()

# Surfaces
background = pygame.image.load('media\graphics\\backgrounds\grass.png')
foreground = pygame.image.load('media\graphics\\backgrounds\grass1.png')
player = pygame.image.load('media\graphics\player\mario-poster.png')
text = font.render("Dino game",False, "#1a2b15")

# Main loop
while running:
    # Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Surfaces init
    screen.blit(background, (0,0))
    screen.blit(foreground, (0,550))
    screen.blit(player, (100, 400))
    screen.blit(text, (300, 300))

    # Refresh
    pygame.display.update()
    
    # Frame rate (ceiling)
    clock.tick(60)