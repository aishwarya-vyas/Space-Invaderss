import pygame 
import random
import math
import time
from pygame import mixer



#initialise game
pygame.init()

#creating screen
width = 800
height = 600
p_w = 64
p_h = 64
screen = pygame.display.set_mode((width,height))

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
bg = pygame.image.load('space.png')

#player
playerImg = pygame.image.load('player.png')
pX = 370
pY = 520 
pX1 = 0
pY1 = 0

#enemy
enemyImg=[]
eX=[]
eY=[]
eX1=[]
eY1=[]
enemies = 6

for i in range(enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    eX.append(random.randint(p_w,width-p_w))
    eY.append(random.randint(0,3*p_h))
    eX1.append(0.2)
    eY1.append(40)

#bullet
bImg = pygame.image.load('bullet.png')
bX = 0
bY = 480
bY1 = 2
bState = 'ready'


score_val=0
life_val = 3
font = pygame.font.Font('freesansbold.ttf',32)
 
txtX = 10
txtY = 10

lifeX = 680
lifeY = 10
 
def show_score(x,y):
    score = font.render("Score: " + str(score_val), True, (255,255,255),)
    screen.blit(score,(x,y))

def show_life(x,y):
    life = font.render("Life: " + str(life_val), True, (255,255,255),)
    screen.blit(life,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def firebullet(x,y):
    global bState
    bState = 'fire'
    screen.blit(bImg,(x + 16,  y + 10))

def isCollision(x1,y1,x2,y2):
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    if dist < 25.4:
        return True
    else:
        return False
#game loop
running = True 
while running:
    screen.fill((0,0,0))
    screen.blit(bg,(0,0)) 
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                pX1 = -0.5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                pX1 = 0.5
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                pY1 = -0.5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pY1 = 0.5
            if event.key == pygame.K_SPACE:
                if bState == 'ready':
                    bX = pX
                    bY = pY
                    firebullet(bX,bY)
                
        if event.type == pygame.KEYUP:
            if  event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_a:
                pX1 = 0
            if  event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pY1 = 0
    
    pX += pX1
    if pX <= 0:
        pX = 0
    elif pX >= 736:
        pX = 736
    pY += pY1
    if pY <= 0:
        pY = 0
    elif pY >=536:
        pY = 536

    for i in range(enemies):
        eX[i] += eX1[i]
        if eX[i] >= 736:
            eX1[i] = -0.3
            eY[i] += eY1[i] 
        elif eX[i] <= 0:
            eX1[i]  =0.3
            eY[i] += eY1[i]
        BEcollision = isCollision(eX[i],eY[i],bX,bY)
        if BEcollision == True:
            bY=480
            bState = 'ready'
            score_val+=1
            print(score_val)
            eX[i] = random.randint(p_w,width-p_w)
            eY[i] = random.randint(0,3*p_h)
    
        PEcollision = isCollision(pX,pY,eX[i],eY[i])
        if PEcollision == True:
            time.sleep(1)
            life_val-=1
            eX[i] = random.randint(p_w,width-p_w)
            eY[i] = random.randint(0,3*p_h)
            pX = 370
            pY = 520 
        enemy(eX[i],eY[i],i)


    if bY <= 0:
        bY =480
        bState = 'ready'

    if bState  == 'fire':
        firebullet(bX,bY)
        bY -= bY1 

    if life_val == 0:
        time.sleep(3)
        life_val = 3
        score_val = 0
        
    show_score(txtX,txtY)
    show_life(lifeX,lifeY)

    player(pX,pY)
    pygame.display.update()