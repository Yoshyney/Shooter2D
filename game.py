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
                break
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            write_text('RETRO SHOOTER', WIDTH / 4 - 10, HEIGHT / 4, WHITE, 18)
            if count / 2 - 10 < 30:
                write_text('Press Enter To Play', WIDTH / 4, HEIGHT / 2, WHITE)
                write_text('Or Escape to quit !', WIDTH / 4 + 10, HEIGHT / 2 + 40, WHITE)
            write_text('made by Steven Chiffe', WIDTH / 4 + 20, HEIGHT - 10, WHITE, 8)
        clock.tick(FPS)
        pygame.display.update()  
    chooseYourShip(menuSong)
    # launch_game()

def write_text(message, x, y, color, fontSize = 12):
    GAME_FONT = pygame.freetype.Font("Assets/font/8-BIT WONDER.TTF", fontSize)
    text, rect = GAME_FONT.render(message, color)
    screen.blit(text, (x, y))


def chooseYourShip(menuSong):
    Numbership = 0
    count = 1
    start = False
    counter = 0
    while True:
        ship = pygame.image.load(pathImage + "Ship/ship" + str(Numbership) + ".png")
        background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
        count = count + 1
        if count == 150:
            count = 1
        event = pygame.event.poll()
        screen.blit(background , (0, 0))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key  ==  pygame.K_LEFT:
                if Numbership != 2:
                    Numbership =  Numbership + 1
            elif event.key  ==  pygame.K_RIGHT:
                if  Numbership != 0:
                    Numbership =  Numbership - 1
            elif event.key  ==  pygame.K_RETURN:
                start = True
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
            screen.blit(ship,(WIDTH / 2 - (ship.get_size()[0] / 2), HEIGHT / 2))
            write_text("Ship number " + str(Numbership), WIDTH / 3 - 10, HEIGHT / 2 + 100, PURPLE)
            write_text("Press enter to go", WIDTH / 3 - 30, HEIGHT / 2 + 130, PURPLE)
        clock.tick(FPS)
        pygame.display.update()
    launch_game(Numbership)


def launch_game(numbership):
    ship = pygame.image.load(pathImage + "Ship/ship" + str(numbership) + ".png")
    ship = pygame.transform.scale(ship, (50, 38))
    laser = pygame.image.load(pathImage  +  "Weapon/laser0.png")
    piou = pygame.mixer.Sound( pathAudio  + 'sfx_laser1.ogg')
    player = Player(ship)
    weapon = Weapon(player)
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
        bullet = weapon.getBullets()
        if len(bullet) != 0:
            for x in bullet:
                screen.blit(laser, (x[0], x[1]))
        if keys[pygame.K_LEFT]:
            player.updateMovement("left")
        if keys[pygame.K_RIGHT]:
            player.updateMovement("right") 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_SPACE:
                if(weapon.pioupiou()):
                    piou.play()      
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        clock.tick(FPS)
        weapon.update()
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

class Weapon:

    def __init__(self, Player):
        self.Player = Player
        self.number = 1
        self.bullets = []
        self.shoot = True
        self.speed = 3
    
    def pioupiou(self):
        if self.shoot:
            self.shoot = False
            self.launchBullet()
            self.bullets.append([self.x + 20, self.y - 30, self.number])
            return True
        return False

    def launchBullet(self):
        self.x = self.Player.getX()
        self.y = self.Player.getY()
    
    def update(self):
        for x in range(0 , len(self.bullets)):
            if x == len(self.bullets) - 1  and self.y - self.bullets[len(self.bullets) - 1][1] > 150:
                self.shoot = True
            self.bullets[x][1] = self.bullets[x][1] - self.speed
        if len(self.bullets) != 0:
            if self.bullets[0][1] < -40:
                del self.bullets[0]
            
    def getBullets(self):
        return self.bullets

init_menu()