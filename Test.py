import pygame
from time import sleep

pygame.init()

font = pygame.font.Font('media/font/GOUDYSTO.TTF', 50)

display = pygame.display.set_mode((800,400))

clock = pygame.time.Clock()

button_surf = pygame.image.load('media/graphics/characters/player/player_crouch.png')
button_rect = button_surf.get_rect(center=(400,300))

text_box_surf = pygame.image.load('media\graphics\characters\player\player.png')
text_box_rect = text_box_surf.get_rect(center=(400,200))

title = font.render("Dino Game", True, (22, 36, 16))
title_rect = title.get_rect(center=(400,100))

text_box_active = False

name = ""

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        if e.type == pygame.MOUSEBUTTONUP:
            if button_rect.collidepoint(mouse_x, mouse_y):
                print("start game")
            if text_box_rect.collidepoint(mouse_x, mouse_y):
                print("text box activated")
                text_box_active = True
        if e.type == pygame.KEYDOWN:
            if text_box_active == True:
                if e.key == pygame.K_RETURN:
                    text_box_active = False
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name+=e.unicode

    display.fill("seagreen4")
    display.blit(title, title_rect)
    display.blit(button_surf, button_rect)
    display.blit(text_box_surf,text_box_rect)

    pygame.draw.rect(display, (0,0,0), pygame.Rect(250, 200, 300, 60))

    text_box = font.render(name, True, (22, 0, 16))
    text_rect = text_box.get_rect(topleft=(200,200))
    display.blit(text_box, text_rect)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    pygame.display.update()

    # ceiling frame rate
    clock.tick(60)