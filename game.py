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
    power = Power_up(weapon, player, meteors)
    score = 0
    count = 1
    while True:
        background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
        count = count + 1
        if count == 150:
            count = 1
        screen.blit(background , (0, 0))
        write_text(str(score), WIDTH / 2, 10, PURPLE)
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        bullet = weapon.getBullets()
        meteor = meteors.getMeteors()
        if len(bullet) != 0:
            for x in bullet:
                screen.blit(laser, (x[0], x[1]))
        for x in meteor:
            screen.blit(x[3], (x[0], x[1]))
        for x in power.powers:
            screen.blit(x[2], (x[0], x[1]))
        screen.blit(ship, (player.getX(), player.getY()))
        if keys[pygame.K_LEFT]:
            player.updateMovement("left")
        if keys[pygame.K_RIGHT]:
            player.updateMovement("right") 
        if keys[pygame.K_SPACE]:
            if(weapon.pioupiou()):
                piou.play()    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()     
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        clock.tick(FPS)
        score = boundaries(player, meteors, weapon, score, power)
        weapon.update()
        power.update()
        meteors.update(score)
        pygame.display.update()     

def boundaries(player, meteors, weapon, score, power):
    lose = pygame.mixer.Sound( pathAudio  + 'sfx_lose.ogg')
    bolt = pygame.mixer.Sound( pathAudio  + 'sfx_zap.ogg')
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
                    power.is_falling(x[0], x[1])
                    if not weapon.shoot:
                        weapon.addDelay(y[1])
                    meteors.meteors.remove(x)
                    weapon.bullets.remove(y)
    for power_ in power.powers:
        powerX = power_[2].get_size()[0]
        powerY = power_[2].get_size()[1]
        if(player.getX() + player.width > power_[0] and player.getX() < power_[0]) or (player.getX() + player.width + power_[0] + powerX and player.getX() < power_[0] + powerX):
            if player.getY() > power_[1] and power_[1] > player.getY() - player.height + 25 or player.getY() > power_[1] - powerY and power_[1] - powerY > player.getY() - player.height:
                score = power.encounter(score, bolt)
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

class Power_up:
    def __init__(self, weapon, player, meteor):
        self.speed = 2
        self.power = ["pill_amo", "pill_speedamo", "pill_speed"]
        self.bold = ["bronze", 'silver', "gold"]
        self.Weapon = weapon
        self.Player = player
        self.Meteors = meteor
        self.powers = []

    def is_falling(self, x , y):
        randomized = random.randrange(0, 100)
        if randomized < 10 and len(self.powers) == 0:
            power = random.choice(self.power)
            image = pygame.image.load(pathImage + "Power/" + power + ".png")
            self.powers.append([x, y , image, power])
        if (randomized == 42 or randomized == 84) and len(self.powers) == 0:
            bolt = random.choice(self.bold)
            image = pygame.image.load(pathImage + "Power/bolt_" + bolt + ".png")
            self.powers.append([x, y , image, bolt])

    def update(self):
        if len(self.powers) != 0:
            self.powers[0][1] = self.powers[0][1] + self.speed
            if self.powers[0][1] > HEIGHT + 10:
                self.powers.pop(0)

    def encounter(self, score, zicmu):
        item = pygame.mixer.Sound( pathAudio  + 'sfx_item.ogg')
        if self.powers[0][3] == "pill_amo":
            self.Weapon.number = self.Weapon.number + 1
            if self.Weapon.number == 3:
                self.power.remove("pill_amo")
        elif self.powers[0][3] == "pill_speedamo":
            self.Weapon.speed = self.Weapon.speed + 1
        elif self.powers[0][3] == "pill_speed":
            self.Player.speed = self.Player.speed + 1
        if self.powers[0][3] == "bronze" or self.powers[0][3] == "silver" or self.powers[0][3] == "gold":
            if self.powers[0][3] == "bronze":
                toDestroy = math.ceil(len(self.Meteors.meteors) / 3)
            elif self.powers[0][3] == "silver":
                toDestroy = math.ceil(len(self.Meteors.meteors) / 2)
            else:
                toDestroy = len(self.Meteors.meteors)
            count = 0
            tab = []
            for x in self.Meteors.meteors:
                if count == toDestroy:
                    break
                Explosion(x[4], x[5], x[0], x[1])
                score = score + math.floor(x[5] / 10)
                tab.append(x)
                count = count + 1
            for x in tab:
               self.Meteors.meteors.remove(x)
            zicmu.play()    
            self.powers.pop(0)
            return score
        item.play()
        self.powers.pop(0)
        return score

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
        self.number = 2
        self.bullets = []
        self.stock = []
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
        if self.stock != 0:
            self.addDelay(0)
    
    def addDelay(self, y):
        if y != 0:
            if len(self.stock) == 0:
                self.stock.append(y)
            if len(self.stock) == 1:
                self.stock[0]  = self.stock[0] - self.speed
                if self.stock[0] > self.distance:
                    self.shoot = True
                    self.stock = []


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