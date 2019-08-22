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
PURPLE = (221, 160, 221)

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
    menuSong = pygame.mixer.Sound( pathAudio  + 'menu.ogg')
    menuSong.play(-1)
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif start:
            if counter <= 60:
                write_text('3', WIDTH / 2 - 10, HEIGHT / 2, WHITE, 50)
            elif counter >= 60 and counter < 120:
                write_text('2', WIDTH / 2 - 10, HEIGHT / 2, WHITE, 50)
            elif counter >= 120 and counter < 180:
                menuSong.stop()
                ready = pygame.mixer.Sound( pathAudio  + 'getready.ogg')
                ready.play()
                write_text('1', WIDTH / 2 - 10, HEIGHT / 2, WHITE, 50)
                write_text('READY', WIDTH / 3 + 10, HEIGHT / 4, WHITE, 20)
            elif counter > 180:
                break
            counter = counter + 1
        else:
            write_text('RETRO SHOOTER', WIDTH / 4 - 10, HEIGHT / 4, WHITE, 18)
            if count / 2 - 10 < 30:
                write_text('Press Enter To Play', WIDTH / 4, HEIGHT / 2, WHITE)
                write_text('Or Escape to quit !', WIDTH / 4 + 10, HEIGHT / 2 + 40, WHITE)
            write_text('made by Steven Chiffe', WIDTH / 4 + 20, HEIGHT - 10, WHITE, 8)
        clock.tick(FPS)
        pygame.display.update()  
    # chooseYourShip()
    launch_game()

def write_text(message, x, y, color, fontSize = 12):
    GAME_FONT = pygame.freetype.Font("Assets/font/8-BIT WONDER.TTF", fontSize)
    text, rect = GAME_FONT.render(message, color)
    screen.blit(text, (x, y))


# def chooseYourShip():
#     Numbership = 0
#     count = 1
#     while True:
#         ship = pygame.image.load(pathImage + "Ship/ship" + str(Numbership) + ".png")
#         background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
#         count = count + 1
#         if count == 150:
#             count = 1
#         screen.blit(background , (0, 0))
#         screen.blit(ship,(WIDTH / 2 - (ship.get_size()[0] / 2), HEIGHT / 2))
#         write_text("Ship number " + str(Numbership), WIDTH / 3 - 10, HEIGHT / 2 + 100, PURPLE)
#         write_text("Press enter to go", WIDTH / 3 - 30, HEIGHT / 2 + 130, PURPLE)
#         event = pygame.event.poll()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 quit()
#             elif event.key  ==  pygame.K_LEFT:
#                 if Numbership != 2:
#                     Numbership =  Numbership + 1
#             elif event.key  ==  pygame.K_RIGHT:
#                 if  Numbership != 0:
#                     Numbership =  Numbership - 1
#         elif event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#         clock.tick(FPS)
#         pygame.display.update()   



def launch_game():
    ship = pygame.image.load(pathImage + "Ship/ship2.png")
    ship = pygame.transform.scale(ship, (50, 38))
    player = Player(ship)
    count = 1
    while True:
        background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
        count = count + 1
        if count == 150:
            count = 1
        screen.blit(background , (0, 0))
        screen.blit(ship, (player.getX(), player.getY()))
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.updateMovement("left")
        if keys[pygame.K_RIGHT]:
            player.updateMovement("right") 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        clock.tick(FPS)
        pygame.display.update()     

class Player:
    def __init__(self, ship_sprite):
        self.x = WIDTH / 2
        self.y = HEIGHT - 50
        self.lives = 3
        self.speed = 2.2
        self.width = ship_sprite.get_size()[0]
        self.height = ship_sprite.get_size()[1]
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def updateMovement(self, where):
        if(where == "right"):
            if(self.width +  self.x  < WIDTH):
                self.x = self.x + self.speed
        else:
            if(self.x > 0):
                self.x = self.x - self.speed
init_menu()