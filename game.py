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
        background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
        count = count + 1
        if count == 150:
            count = 1
        event = pygame.event.poll()
        screen.blit(background , (0, 0))
        plus = 0
        for x in range(0, 6):
            ship = pygame.image.load(pathImage + "Ship_selection/ship" + str(x) + ".png")
            screen.blit(ship,(WIDTH / 4 - 30 + plus, HEIGHT / 2))
            if x == Numbership:
                pygame.draw.rect(screen , PURPLE, (WIDTH / 4 - 30 + plus,  HEIGHT / 2 + 33 , ship.get_size()[0] , 5) )
            plus = plus + 40
        if event.type == pygame.KEYDOWN and not start:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key  ==  pygame.K_RIGHT and not start:
                if Numbership != 5:
                    Numbership =  Numbership + 1
            elif event.key  ==  pygame.K_LEFT and not start:
                if  Numbership != 0:
                    Numbership =  Numbership - 1
            elif event.key  ==  pygame.K_RETURN:
                start = True
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif start:
            if counter <= 60:
                write_text('3', WIDTH / 2 - 10, HEIGHT / 4, WHITE, 50)
            elif counter >= 60 and counter < 120:
                write_text('2', WIDTH / 2 - 10, HEIGHT / 4, WHITE, 50)
            elif counter >= 120 and counter < 180:
                menuSong.stop()
                ready = pygame.mixer.Sound( pathAudio  + 'getready.ogg')
                ready.play()
                write_text('1', WIDTH / 2 - 10, HEIGHT / 4, WHITE, 50)
                write_text('READY', WIDTH / 3 + 10, HEIGHT / 4 + 60, WHITE, 20)
            elif counter > 180:
                break
            counter = counter + 1
        if not start:
            pygame.draw.rect(screen , PURPLE, (WIDTH / 2 - 90, HEIGHT / 2 + 80 ,WIDTH / 2, 30))
            if text_boundaries("Return", WIDTH / 2 - 80, HEIGHT / 2 + 90):
                write_text("Return", WIDTH / 2 - 80, HEIGHT / 2 + 90, BLACK)
                if pygame.mouse.get_pressed()[0] == 1:
                    menuSong.stop()
                    init_menu()
            else:
                write_text("Return", WIDTH / 2 - 80, HEIGHT / 2 + 90, WHITE)
            if text_boundaries("Choose", WIDTH / 2 + 10, HEIGHT / 2 + 90):
                write_text("Choose", WIDTH / 2 + 10, HEIGHT / 2 + 90, BLACK)
                if pygame.mouse.get_pressed()[0] == 1:
                    start = True
            else:
                write_text("Choose", WIDTH / 2 + 10, HEIGHT / 2 + 90, WHITE) 
        clock.tick(FPS)
        pygame.display.update()
    return launch_game(Numbership)


def launch_game(numbership):
    ship = pygame.image.load(pathImage + "Ship/ship" + str(numbership) + ".png")
    ship = pygame.transform.scale(ship, (50, 38))
    laser = pygame.image.load(pathImage  +  "Weapon/laser0.png")
    piou = pygame.mixer.Sound( pathAudio  + 'sfx_laser1.ogg')
    player = Player(ship, numbership)
    weapon = Weapon(player)
    meteors = Meteors()
    power = Power_up(weapon, player, meteors)
    enemy = Enemy()
    score = 0
    count = 1
    while True:
        background = pygame.image.load(pathImage + "Background/background" + str(math.floor(count / 10)) + ".gif")
        count = count + 1
        if count == 150:
            count = 1
        screen.blit(background , (0, 0))
        write_text(str(score), WIDTH / 2, 10, WHITE)
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        bullet = weapon.getBullets()
        meteor = meteors.getMeteors()
        if len(bullet) != 0:
            for x in bullet:
                screen.blit(laser, (x[0], x[1]))
        for x in meteor:
            screen.blit(x[3], (x[0], x[1]))
        for x in enemy.enemy:
            screen.blit(x[2], (x[0], x[1]))
        for x in enemy.bullets:
            screen.blit( x[2],(x[0], x[1]))
        for x in power.powers:
            screen.blit(x[2], (x[0], x[1]))
        screen.blit(ship, (player.getX(), player.getY()))
        for x in power.shield_:
            screen.blit(x[2], (x[0], x[1]))
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
            elif event.key == pygame.K_RETURN:
                Menu(numbership)
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()   
        score = boundaries(player, meteors, weapon, score, power, numbership, enemy)
        weapon.update()
        power.update()
        meteors.update(score)
        enemy.update(score)
        pygame.display.update()

def Menu(numbership):
    pause = True
    while pause:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_RETURN:
                pause = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.draw.rect(screen , PURPLE, (120,220,140,150) )
        if text_boundaries("Continue", WIDTH / 2 - 45, HEIGHT / 2):
            write_text("Continue", WIDTH / 2 - 45, HEIGHT / 2, BLACK)
            if pygame.mouse.get_pressed()[0] == 1:
                pause = False
        else :
             write_text("Continue", WIDTH / 2 - 45, HEIGHT / 2, WHITE)
        if text_boundaries("Replay", WIDTH / 2 - 45, HEIGHT / 2 + 30):
            write_text("Replay", WIDTH / 2 - 45, HEIGHT / 2 + 30, BLACK)
            if pygame.mouse.get_pressed()[0] == 1:
                launch_game(numbership)
        else:
            write_text("Replay", WIDTH / 2 - 45, HEIGHT / 2 + 30, WHITE)
        if text_boundaries("Go to Menu", WIDTH / 2 - 45, HEIGHT / 2 + 60):
            write_text("Go to Menu", WIDTH / 2 - 45, HEIGHT / 2 + 60, BLACK)
            if pygame.mouse.get_pressed()[0] == 1:
                init_menu()
        else:
            write_text("Go to Menu", WIDTH / 2 - 45, HEIGHT / 2 + 60, WHITE)
        if text_boundaries("Quit", WIDTH / 2 - 45, HEIGHT / 2 + 90):
            write_text("Quit", WIDTH / 2 - 45, HEIGHT / 2 + 90, BLACK)
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                quit()
        else:
            write_text("Quit", WIDTH / 2 - 45, HEIGHT / 2 + 90, WHITE)
        clock.tick(FPS)
        pygame.display.update()

def text_boundaries(Text, x, y):
    text_len = len(Text)
    sourisX = pygame.mouse.get_pos()[0]
    sourisY = pygame.mouse.get_pos()[1]
    if x <= sourisX and x + (text_len * 11) >= sourisX:
        if y <= sourisY and y + 9 >= sourisY:
            return True
    return False

def lost_menu(numbership, score):
    pause = True
    stars = 0
    if score > 500:
        stars = stars + 1
    if score > 1500:
        stars = stars + 1
    if score > 5000:
        stars = stars + 1
    while pause:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        y = 0
        pygame.draw.rect(screen , PURPLE, (120,185,135,170) )
        write_text("Score  " + str(score) , WIDTH / 2 - 45, HEIGHT / 2 , WHITE)
        for x in range(0 , stars):
            star = pygame.image.load(pathImage  +  "star/star_" +  str(x) + ".png")
            screen.blit(star, (130 + y, HEIGHT / 2 - 45) )
            y = y + 30
        if stars == 0:
            write_text("No stars", WIDTH / 2 - 45, HEIGHT / 2 - 30, WHITE)
        if text_boundaries("Replay", WIDTH / 2 - 45, HEIGHT / 2 + 30):
            write_text("Replay", WIDTH / 2 - 45, HEIGHT / 2 + 30, BLACK)
            if pygame.mouse.get_pressed()[0] == 1:
                launch_game(numbership)
        else:
            write_text("Replay", WIDTH / 2 - 45, HEIGHT / 2 + 30, WHITE)
        if text_boundaries("Go to Menu", WIDTH / 2 - 45, HEIGHT / 2 + 60):
            write_text("Go to Menu", WIDTH / 2 - 45, HEIGHT / 2 + 60, BLACK)
            if pygame.mouse.get_pressed()[0] == 1:
                init_menu()
        else:
            write_text("Go to Menu", WIDTH / 2 - 45, HEIGHT / 2 + 60, WHITE)
        if text_boundaries("Quit", WIDTH / 2 - 45, HEIGHT / 2 + 90):
            write_text("Quit", WIDTH / 2 - 45, HEIGHT / 2 + 90, BLACK)
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                quit()
        else:
            write_text("Quit", WIDTH / 2 - 45, HEIGHT / 2 + 90, WHITE)
        clock.tick(FPS)
        pygame.display.update()

def boundaries(player, meteors, weapon, score, power, numbership, enemy):
    lose = pygame.mixer.Sound( pathAudio  + 'sfx_lose.ogg')
    bolt = pygame.mixer.Sound( pathAudio  + 'sfx_zap.ogg')
    shield = pygame.mixer.Sound( pathAudio  + 'sfx_shieldDown.ogg')
    for x in meteors.meteors:
        if (player.getX() + player.width > x[0] and player.getX() < x[0]) or (player.getX() + player.width > x[0] + x[4] and player.getX() < x[0] + x[4]) or (player.getX() + player.width > x[0] and (player.getX() < x[0] + x[4] / 2 or player.getX() < x[0] + x[4] / 3)):
            if player.getY() > x[1] and x[5] <= 60 and x[5] >= 20 and x[1] > player.getY() - player.height + 30 or player.getY() > x[1] and x[5] >= 60 and x[1] > player.getY() - player.height - 15 or player.getY() > x[1] and x[5] < 20 and x[1] > player.getY() - player.height + 33:
                if player.lives > 1:
                    Explosion(x[4], x[5], x[0], x[1])
                    if x in meteors.meteors:
                        meteors.meteors.remove(x)
                        player.lives = player.lives - 1
                        power.shield_.pop(0)
                        shield.play()
                else :
                    lose.play()
                    lost_menu(numbership, score)
        for y in weapon.bullets:
            if (x[0] < y[0] and x[0] + x[4] > y[0]) or (x[0] < y[0] + weapon.width and x[0] + x[4] > y[0] + weapon.width):
                # correction to do on the impact of the bullet 
                if y[1] + weapon.height < x[1] and ((x[1] - x[5] < y[1]) or (x[1] - x[5] < y[1] + weapon.height)):
                    score = score + math.floor(x[5] / 10)
                    Explosion(x[4], x[5], x[0], x[1])
                    power.is_falling(x[0], x[1])
                    if player.getY() - weapon.bullets[len(weapon.bullets) - 1][1] <= 150:
                        weapon.addDelay(weapon.bullets[len(weapon.bullets) - 1][1])
                    if x in meteors.meteors:
                        meteors.meteors.remove(x)
                    weapon.bullets.remove(y)
    for power_ in power.powers:
        powerX = power_[2].get_size()[0]
        powerY = power_[2].get_size()[1]
        if(player.getX() + player.width > power_[0] and player.getX() < power_[0]) or (player.getX() + player.width + power_[0] + powerX and player.getX() < power_[0] + powerX):
            if player.getY() > power_[1] and power_[1] > player.getY() - player.height + 25 or player.getY() > power_[1] - powerY and power_[1] - powerY > player.getY() - player.height:
                score = power.encounter(score, bolt)
    if len(enemy.enemy) > 0:
        for x in weapon.bullets:
            for y in enemy.enemy:
                if y[0] < x[0] and y[0] + y[3] > x[0] or y[0] < x[0] + weapon.width and y[0] + y[3] > x[0] + weapon.width:
                    if x[1] > y[1] and x[1] < y[1] + y[4] or x[1] - weapon.height > y[1] and x[1] - weapon.height < y[1] + y[4]:
                        if y[5] == 1:
                            Explosion(y[3], y[4], y[0], y[1])
                            enemy.enemy.remove(y)
                        else:
                            if x in weapon.bullets:
                                weapon.bullets.remove(x)
                                y[5] = y[5] - 1
                                Explosion(y[3], y[4], y[0], y[1], 8)
                        score = score + 10
    for x in enemy.bullets:
        if player.getX() < x[0] and player.getX() + player.width > x[0] or player.getX() < x[0] + enemy.width and player.getX() + player.width > x[0] + enemy.width:
            if player.getY() > x[1] and player.getY() - player.height < x[1] or player.getY() > x[1] - enemy.height and player.getY() - player.height < x[1] - enemy.height:
                if player.lives > 1:
                    player.lives = player.lives - 1
                    shield.play()
                    power.shield_.pop(0)
                    if x in enemy.bullets:
                        enemy.bullets.remove(x)
                else :
                    lose.play()
                    lost_menu(numbership, score)
    return score

class Explosion:
    def __init__(self, x, y , positionX, positionY, boom = 12):
        self.positionX = positionX
        self.positionY = positionY
        self.x = x
        self.y = y
        self.boom(boom)

    def boom(self, boom):
        for x in range(0, boom):
                    self.image = pygame.image.load(pathImage + "Explosion/explosion" + str(x) + ".png")
                    self.image = pygame.transform.scale(self.image, (self.x, self.y))
                    screen.blit(self.image, (self.positionX, self.positionY))

class Power_up:
    def __init__(self, weapon, player, meteor):
        self.speed = 2
        self.power = ["pill_amo", "pill_speedamo", "pill_speed"]
        self.bold = ["bronze", 'silver', "gold"]
        self.shield = "shield_gold"
        self.shield_ = []
        self.image = pygame.image.load(pathImage  +  "shield/shield3.png")
        self.shield_image = pygame.transform.scale(self.image, (50, 38))
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
        elif (randomized == 42 or randomized == 84) and len(self.powers) == 0:
            bolt = random.choice(self.bold)
            image = pygame.image.load(pathImage + "Power/bolt_" + bolt + ".png")
            self.powers.append([x, y , image, bolt])
        elif randomized == 37 and len(self.powers) == 0 and self.Player.lives <= 1:
            image = pygame.image.load(pathImage + "Power/" + self.shield + ".png")
            self.powers.append([x, y , image, self.shield])

    def update(self):
        if len(self.powers) != 0:
            self.powers[0][1] = self.powers[0][1] + self.speed
            if self.powers[0][1] > HEIGHT + 10:
                self.powers.pop(0)
        if len(self.shield_) > 0:
            self.shield_.clear()
            self.shield_.append([self.Player.getX(), self.Player.getY(), self.shield_image])

    def encounter(self, score, zicmu):
        item = pygame.mixer.Sound( pathAudio  + 'sfx_item.ogg')
        shield = pygame.mixer.Sound( pathAudio  + 'sfx_shieldUp.ogg')
        if self.powers[0][3] == "pill_amo":
            self.Weapon.number = self.Weapon.number + 1
            if self.Weapon.number == 3:
                self.power.remove("pill_amo")
        elif self.powers[0][3] == "pill_speedamo":
            self.Weapon.speed = self.Weapon.speed + 1
        elif self.powers[0][3] == "pill_speed":
            self.Player.speed = self.Player.speed + 1
        elif self.powers[0][3] == "shield_gold":
            self.Player.lives = self.Player.lives + 1
            self.shield_.append([self.Player.getX(), self.Player.getY(), self.shield_image])
            shield.play()
            self.powers.pop(0)
            return score
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


class Enemy:
    def __init__(self):
        self.enemyShip = ["enemyBlack_2", "enemyBlue_1", "enemyGreen_1", "enemyRed_3"]
        self.enemy = []
        self.bullets = []
        self.bulletSpeed = 4
        self.possible = 1
        self.speedY = 4
        self.speedX = 5
        self.value = 500
        self.bool = True
        self.last_update = pygame.time.get_ticks()
        self.updated = pygame.time.get_ticks()
        self.width = pygame.image.load(pathImage  +  "Weapon/laser1.png").get_size()[0]
        self.height =  pygame.image.load(pathImage  +  "Weapon/laser1.png").get_size()[1]

    def apparition(self):
        randomized = random.randrange(0, 100)
        actual_time = pygame.time.get_ticks()
        if len(self.enemy) < self.possible and randomized < 25 and actual_time - self.last_update > 4000:
            Enemy = random.choice(self.enemyShip)
            lives = Enemy.split("_")[1]
            Enemy = pygame.image.load(pathImage + "Enemy/" + Enemy + ".png")
            EnemyX = Enemy.get_size()[0]
            EnemyY = Enemy.get_size()[1]
            PositionX = random.randrange(0, WIDTH - EnemyX)
            PositionY = random.randrange(-300, -100)
            self.enemy.append([PositionX, PositionY , Enemy, EnemyX, EnemyY, int(lives)])

    def update(self, score):
        shoot = False
        for x in self.enemy:
            self.last_update = pygame.time.get_ticks()
            if x[1] <  10:
                x[1] = x[1] + self.speedY
            else:
                if(self.bool):
                    x[0] = x[0] + self.speedX
                    if x[0] + x[3] >= WIDTH:
                        self.bool = False
                else:
                    x[0] = x[0] - self.speedX
                    if x[0] <= 0:
                        self.bool = True
            actual_time = pygame.time.get_ticks()
            if actual_time - self.updated > 2000:
                image = pygame.image.load(pathImage  +  "Weapon/laser1.png")
                diff = 0
                for y in range(0, x[5]):
                    self.bullets.append([x[0] + diff, x[1] + 20, image])
                    diff = diff + 20
                shoot = True
        for x in self.bullets:
            x[1] = x[1] + self.bulletSpeed
            if x[1] > HEIGHT + 50:
                self.bullets.remove(x)
        if score >= self.value:
            self.possible = self.possible + 1
            self.value = self.value + self.value
        if shoot == True:
            self.updated = pygame.time.get_ticks()
        self.apparition()

class Player:
    def __init__(self, ship_sprite, numbership):
        self.x = WIDTH / 2
        self.y = HEIGHT - 50
        self.lives = 1
        self.speed = 5
        if numbership < 3:
            self.width = ship_sprite.get_size()[0]
            self.height = ship_sprite.get_size()[1]
        else:
            self.width = ship_sprite.get_size()[0] - 10
            self.height = ship_sprite.get_size()[1] - 8
    
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
                self.stock = []
            self.bullets[x][1] = self.bullets[x][1] - self.speed
        if len(self.bullets) != 0:
            if self.bullets[0][1] < -40:
                del self.bullets[0]
        if self.stock != 0:
            self.addDelay(0)
    
    def addDelay(self, y):
        if len(self.stock) == 0 and y != 0:
            self.stock.append(y)
        if len(self.stock) == 1:
            self.stock[0] = self.stock[0] - self.speed
            if self.y - self.stock[0] > self.distance:
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
            if self.meteors[x][1] > HEIGHT + 50:
                tab.append(self.meteors[x])
        for x in tab:
            self.meteors.remove(x)
        if score > self.more:
            self.add  = self.add + 1
            self.more =  self.more + 100
        if len(self.meteors) < self.add:
            self.generation(self.add - len(self.meteors))


    def getMeteors(self):
        return self.meteors
    
    def setMeteors(self, tab):
        self.meteors = tab
    
init_menu()