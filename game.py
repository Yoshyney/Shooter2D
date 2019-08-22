import pygame
import random
import pygame.freetype
import math

WIDTH = 360
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter 2d")
clock = pygame.time.Clock()
pathImage = "Assets/Image/"
pathAudio = "Assets/Audio/"

def init_menu():
    count = 1
    start = False
    counter = 0
    while True:
        background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
        count = count + 1
        if count == 150:
            count = 1
        screen.blit(background , (0, 0))
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = True
            elif event.key == pygame.K_q:
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif start:
            if counter <= 60:
                write_text('3', WIDTH / 2 - 5, HEIGHT / 2, WHITE, 30)
            elif counter >= 60 and counter < 120:
                write_text('2', WIDTH / 2 - 10, HEIGHT / 2, WHITE, 40)
            elif counter >= 120 and counter < 180:
                write_text('1', WIDTH / 2 - 10, HEIGHT / 2, WHITE, 50)
                write_text('READY', WIDTH / 3 + 10, HEIGHT / 4, WHITE, 20)
            elif counter > 180:
                break
            counter = counter + 1
        else:
            write_text('RETRO SHOOTER', WIDTH / 4, HEIGHT / 4, WHITE, 18)
            if count / 2 - 10 < 30:
                write_text('Press Enter To Play', WIDTH / 4, HEIGHT / 2, WHITE)
            write_text('made by Steven Chiffe', WIDTH / 4 + 20, HEIGHT - 10, WHITE, 8)
        clock.tick(FPS)
        pygame.display.update()

def write_text(message, x, y, color, fontSize = 12):
    GAME_FONT = pygame.freetype.Font("Assets/font/8-BIT WONDER.TTF", fontSize)
    text, rect = GAME_FONT.render(message, color)
    screen.blit(text, (x, y))

init_menu()