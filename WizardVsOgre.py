#import libraries
import pygame
import random
import math
from pygame import mixer

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#set title and icon that appear at top of window
pygame.display.set_caption('Wizard Vs. Ogre')
icon = pygame.image.load('alchemy.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('castle.jpg')

# background music (-1 indicates it will loop)
mixer.music.load('background.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.3)

#player values
playerImg = pygame.image.load('wizard.png')
playerX = 360
playerY = 540
playerX_change = 0
playerY_change = 0

#draws player on screen with info defined above
def player(x,y):
    screen.blit(playerImg, (x, y))

#enemy values 
#(empty lists created for multiple enemies. for loop used to fill the lists with x amount of enemies by appending)

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ogre.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(20)
    enemyX_change.append(0.3)
    enemyY_change.append(64)

#fireball values
fireballImg = pygame.image.load('fireball.png')
fireballX = 0
fireballY = 540
fireballX_change = 0
fireballY_change = 1
fireball_state = "ready"

#draws enemy on screen
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

#score values
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#function used to display the score
def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

#game over text values
over_font = pygame.font.Font('freesansbold.ttf',64)

#function used to diplay the game over text
def game_over_text():
    over_text = over_font.render("YOU DIED",True, (255,255,255))
    screen.blit(over_text,(200,250))

#function for wizard shooting fireball
def shoot_fireball(x,y):
    global fireball_state
    fireball_state = "fire"
    screen.blit(fireballImg,(x,y))

#function that determines if the fireball will hit an enemy
def isCollision(enemyX,enemyY,fireballX,fireballY):
    distance = math.sqrt((math.pow(enemyX - fireballX,2)) + (math.pow(enemyY - fireballY, 2)))
    if distance < 40:
        return True
    else:
        return False



####### game loop #######

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check what it is
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if fireball_state == 'ready':
                    fireball_sound = mixer.Sound('shoot.wav')
                    fireball_sound.play()
                    fireballX = playerX
                    shoot_fireball(fireballX,fireballY) 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #fills screen with RGB values
    screen.fill((100, 100, 152))
    #adds in background image
    screen.blit(background,(80,0))

    #adds movement values to players x axis
    playerX += playerX_change
    playerY += playerY_change

    #defines boundries for player
    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    if playerY <=0:
        playerY = 0
    elif playerY >= 536:
        playerY = 539

    

    #defines boundries and movement pattern for enemies
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 540:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #collision
        collision = isCollision(enemyX[i],enemyY[i],fireballX,fireballY)
        if collision:
            grunt_sound = mixer.Sound('grunt.wav')
            grunt_sound.play()
            fireballY = 540
            fireball_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = 30
    
        enemy(enemyX[i],enemyY[i], i)


    #fireball movement
    if fireballY <=0:
        fireballY = 540
        fireball_state = "ready"

    if fireball_state == "fire":
        shoot_fireball(fireballX,fireballY)
        fireballY -= fireballY_change

    

   
    player(playerX,playerY) 
    show_score(textX,textY)
    pygame.display.update()