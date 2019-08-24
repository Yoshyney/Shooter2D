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
    meteors = Meteors()
    score = 0
    count = 1
    while True:
        background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
        count = count + 1
        if count == 150:
            count = 1
        screen.blit(background , (0, 0))
        write_text(str(score), WIDTH / 2, 10, PURPLE)
        screen.blit(ship, (player.getX(), player.getY()))
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        bullet = weapon.getBullets()
        meteor = meteors.getMeteors()
        if len(bullet) != 0:
            for x in bullet:
                screen.blit(laser, (x[0], x[1]))
        for x in meteor:
            screen.blit(x[3], (x[0], x[1]))
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
        score = boundaries(player, meteors, weapon, score)
        weapon.update()
        meteors.update(score)
        pygame.display.update()     

def boundaries(player, meteors, weapon, score):
    lose = pygame.mixer.Sound( pathAudio  + 'sfx_lose.ogg')
    for x in meteors.meteors:
        if (player.getX() + player.width > x[0] and player.getX() < x[0]) or (player.getX() + player.width > x[0] + x[4] and player.getX() < x[0] + x[4]) or (player.getX() + player.width > x[0] and (player.getX() < x[0] + x[4] / 2 or player.getX() < x[0] + x[4] / 3)):
            if player.getY() > x[1] and x[5] <= 60 and x[1] > player.getY() - player.height + 25 or player.getY() > x[1] and x[5] >= 60 and x[1] > player.getY() - player.height - 25:
                lose.play()
                launch_game(2)
        for y in weapon.bullets:
            if (x[0] < y[0] and x[0] + x[4] > y[0]) or (x[0] < y[0] + weapon.width and x[0] + x[4] > y[0] + weapon.width):
                # correction to do on the impact of the bullet 
                if y[1] + weapon.height < x[1] and ((x[1] - x[5] < y[1]) or (x[1] - x[5] < y[1] + weapon.height)):
                    score = score + math.floor(x[5] / 10)
                    Explosion(x[4], x[5], x[0], x[1])
                    meteors.meteors.remove(x)
                    weapon.bullets.remove(y)
    return score

class Explosion:
    def __init__(self, x, y , positionX, positionY):
        self.positionX = positionX
        self.positionY = positionY
        self.x = x
        self.y = y
        self.boom()

    def boom(self):
        for x in range(0, 12):
                    self.image = pygame.image.load(pathImage + "Explosion/explosion" + str(x) + ".png")
                    self.image = pygame.transform.scale(self.image, (self.x, self.y))
                    screen.blit(self.image, (self.positionX, self.positionY))

# class Power_up:
#     def __init__(self, weapon, player):
#         self.speed = 2
    
#     def is_falling(self):


class Player:
    def __init__(self, ship_sprite):
        self.x = WIDTH / 2
        self.y = HEIGHT - 50
        self.lives = 3
        self.speed = 5
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
        self.speed = 6
        self.distance = 150
        self.width = pygame.image.load(pathImage  +  "Weapon/laser0.png").get_size()[0]
        self.height =  pygame.image.load(pathImage  +  "Weapon/laser0.png").get_size()[0]
    
    def pioupiou(self):
        if self.shoot and self.number == 1:
            self.shoot = False
            self.launchBullet()
            self.bullets.append([self.x + 20, self.y - 30, self.number])
            return True
        elif self.shoot and self.number == 2: 
            self.shoot = False
            self.launchBullet()
            self.bullets.append([self.x, self.y - 10, self.number])
            self.bullets.append([self.x + 40, self.y - 10, self.number])
            return True
        elif self.shoot and self.number == 3:
            self.shoot = False
            self.launchBullet()
            self.bullets.append([self.x, self.y - 10, self.number])
            self.bullets.append([self.x + 20, self.y - 30, self.number])
            self.bullets.append([self.x + 40, self.y - 10, self.number])
            return True
        return False

    def launchBullet(self):
        self.x = self.Player.getX()
        self.y = self.Player.getY()
    
    def update(self):
        for x in range(0 , len(self.bullets)):
            if x == len(self.bullets) - 1  and self.y - self.bullets[len(self.bullets) - 1][1] > self.distance:
                self.shoot = True
            self.bullets[x][1] = self.bullets[x][1] - self.speed
        if len(self.bullets) != 0:
            if self.bullets[0][1] < -40:
                del self.bullets[0]
        if len(self.bullets) == 0:
            self.shoot = True
            
    def getBullets(self):
        return self.bullets
    
    def setBullets(self, tab):
        self.bullets = tab

class Meteors:
    def __init__(self):
        self.meteors = []
        self.meteorpossible = ["meteor0", "meteor1", "meteor2","meteor3", "meteor4", "meteor5", "meteor6"]
        self.generation()
        self.add = 8
        self.more = 100
        
    def generation(self, range_ = 8):
        for x in range(1 , range_):
            Meteor = random.choice(self.meteorpossible)
            Meteor = pygame.image.load(pathImage + "meteors/" + Meteor + ".png")
            meteorX = Meteor.get_size()[0]
            meteorY = Meteor.get_size()[1]
            PositionX = random.randrange(0, WIDTH - meteorX)
            PositionY = random.randrange(-300, -100)
            Speed = random.randrange(3 , 7)
            self.meteors.append([PositionX, PositionY , Speed, Meteor, meteorX, meteorY])
    
    def update(self, score):
        tab = []
        for x in range(0 , len(self.meteors)):
            self.meteors[x][1] = self.meteors[x][1] + self.meteors[x][2]
            if self.meteors[x][1] + 10 > HEIGHT:
                tab.append(x)
        y = 0
        for x in tab:
            self.meteors.pop(x - y)
            y = y - 1
        if score > self.more:
            self.add  = self.add + 1
            self.more =  self.more + 100
        if len(self.meteors) < self.add:
            self.generation(self.add - len(self.meteors))


    def getMeteors(self):
        return self.meteors
    
    def setMeteors(self, tab):
        self.meteors = tab
# init_menu()
launch_game(2)