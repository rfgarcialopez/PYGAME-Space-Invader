# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 17:26:28 2022

@author: rorro
"""

# Install pygame
#!pip install pygame

# Import libraries
import pandas as pd
import numpy as np
import random
import copy
import math
import pygame

# Initiate the pygame
pygame.init()

# Create the screen
screen=pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Lali Invader")
icon=pygame.image.load('lali.png')
icon.get_size()
icon32=pygame.transform.scale(icon,(32,32))
icon32.get_size()
pygame.display.set_icon(icon32)

# Backgroud
background=pygame.image.load('background.png')
background32=pygame.transform.scale(background,(800,600))


# Player
playerimage=icon32
playerX= 370
playerY= 480
player_change=0

# Enemy

enemy=pygame.image.load('ro.png')
enemy32=pygame.transform.scale(enemy,(32,32))

enemyimage=[]
enemyX= []
enemyY= []
enemyX_change=[]
enemyY_change=[]
num_enemies=6

for i in range (num_enemies):
    enemyimage.append(enemy32)
    enemyX.append(random.randint(0,730))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(10)

# Bullets
bullet=pygame.image.load('bullet.png')
bulletX= 0
bulletY= 480
BulletX_change=0
bulletY_change=1
bullet_state="ready"
# "ready":bullet dont shooted,"fire": bullet already shoot

# Draw an image on the surface
def player(x,y):
    screen.blit(playerimage, (x, y))

def enemy(x,y, i):
    screen.blit(enemyimage[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x+16,y+10))
    
def IsCollision(enemyX,enemyY, bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False

# Score
Score_value = 0
font=pygame.font.Font('freesansbold.ttf',50)
testX=10
testY=10

def show_score(x,y):
    score=font.render("Score:" + str(Score_value), True,(255,215,215))
    screen.blit(score, (x, y))
    
def gameovertext():
    score=font.render("GAME OVER - Score:" + str(Score_value), True,(255,215,215))
    screen.blit(score, (200, 250))
    

# Sound
pygame.mixer.music.load('momentsofclarity.mp3')
pygame.mixer.music.play(-1)
bullet_sound=pygame.mixer.Sound('laser.wav')
explosion_sound=pygame.mixer.Sound('explosion.wav')

# Game Loop
running = True
while running:
    
    screen.fill((0,0,0))
    screen.blit(background32, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                print('left')
                player_change=-0.4
            if event.key==pygame.K_RIGHT:
                print('right')
                player_change=0.4
            if event.key==pygame.K_SPACE:
                if bullet_state == "ready":
                    print('shoot')
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
                    bullet_sound.play()
        if event.type==pygame.KEYUP:
            print('key release')
            player_change=0

# Player movement and boundaries
    playerX+=player_change
    player(playerX,playerY)
    if playerX<=0:
        playerX=0
    if playerX>=768:
        playerX=768

# Enemy movement and boundaries
    for i in range (num_enemies):
        #Game over
        if enemyY[i]>440:
            for j in range (num_enemies):
                enemyY[j]=2000
            gameovertext()
            break
        
        #Game continues
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=0.5
            enemyY[i]+=enemyY_change[i]
        if enemyX[i]>=768:
            enemyX_change[i]=-0.5
            enemyY[i]+=enemyY_change[i]
            
        collision=IsCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound.play()
            bulletY=480
            bullet_state='ready'
            Score_value += 1
            print ('BOOOOM!!!!' + str(Score_value))
            enemyX[i]= random.randint(0,730)
            enemyY[i]= random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)

#Bullet movement
    if bulletY < 0:
        bulletY = 480
        bullet_state="ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY-= bulletY_change
        
    show_score(testX, testY)

    pygame.display.update()
    
    
pygame.quit()