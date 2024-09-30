import pygame
import random
import math
from pygame_recorder import ScreenRecorder
import numpy as np
from Car import Car
from Wall import Wall
from Ball import Ball
from Agent import Agent

pygame.init()
screen = pygame.display.set_mode((1280, 900))
clock = pygame.time.Clock()
running = True

AI = True
secondstorecord = 600

recorder = ScreenRecorder(1280, 900, 40,"./videos/output.avi")

class Goal:
    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos, size)
        self.score = 0
        self.color = (255, 0, 0)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collision(self, ball):
        if self.rect.colliderect(ball.hitbox):
            self.score += 1
            # self.reset()
            ball.pos = (635,345)
            ball.vel = pygame.Vector2(0,0)

    def ballcollision(self,ball):
        if self.rect.colliderect(pygame.Rect(ball.pos,(ball.image.get_width(),ball.image.get_height()))):
            ball.pos = ball.pos
            ball.vel = ball.vel.reflect(self.normal)


cars = []
cars.append(Car((300,300)))
if(AI):
    ag = Agent(cars[0],False)

walls = []
walls.append(Wall((10,10),(1250,20),pygame.Vector2(0,-1)))
walls.append(Wall((10,670),(1250,20),pygame.Vector2(0,1)))
walls.append(Wall((10,10),(20,680),pygame.Vector2(-1,0)))
walls.append(Wall((1250,10),(20,680),pygame.Vector2(1,0)))


wpressed = False
apressed = False
spressed = False
dpressed = False

# reward = 0
class target:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def render(self,screen):
        pygame.draw.circle(screen,(255,255,255),(self.x,self.y),10)

    def collision(self,car):
        if pygame.Rect(self.x-10,self.y-10,20,20).colliderect(car.hitbox):
            self.x = random.randint(100,1150)
            self.y = random.randint(100,620)
            car.reward += 50000

t = target(500,500)
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

frame = 0
saved = False
while running:

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(120) / 1000
    if(AI):
        dt = 0.008

    #AIblock
    if(AI):
        state = np.array([t.x-cars[0].pos.x,t.y-cars[0].pos.y,cars[0].vel.x,cars[0].vel.y,cars[0].heading.x,cars[0].heading.y,cars[0].pos.x,cars[0].pos.y]).reshape((1,-1))
        # state = np.array([cars[0].pos.x/1280,cars[0].pos.y/700,cars[0].vel.x/520,cars[0].vel.y/520,t.x/1280,t.y/700]).reshape((1,-1))
        action = ag.getaction(state)
        wpressed,spressed,dpressed,apressed = Agent.decodeaction(action)

    else:
        keys = pygame.key.get_pressed()
        wpressed = keys[pygame.K_w]
        apressed = keys[pygame.K_a]
        spressed = keys[pygame.K_s]
        dpressed = keys[pygame.K_d]
    
    #RewardBlock
    cars[0].reward =-1
    cars[0].reward +=  math.exp(-(((cars[0].pos - pygame.Vector2(t.x,t.y)).length())/1))
    cars[0].reward = cars[0].reward*120 - 80
    cars[0].reward += ((-pygame.Vector2(t.x,t.y) + cars[0].pos).normalize()).dot(cars[0].heading)*100
    


    #UpdateBlock
    cars[0].tick(dt,wpressed,spressed,dpressed,apressed)    
    for w in walls:
        for c in cars:
            w.collision(c,dt)
    t.collision(cars[0])
    cars[0].score += cars[0].reward*0.01
    if(frame%(3 if AI else 1) == 0):
        #RenderBlock
        screen.fill((0,0,0))
        t.render(screen)
        for c in cars:
            c.render(screen)
        for w in walls:
            w.render(screen)
        text = font.render('Score: '+"{:.2f}".format(cars[0].score), True, (255, 255, 255))
        screen.blit(text,(1000,730))
        text = font.render('Reward: '+"{:.2f}".format(cars[0].reward), True, (255, 255, 255))
        screen.blit(text,(1000,750))
        if(AI):
            text = font.render('Last Loss: '+"{:.2f}".format(ag.lastloss), True, (255, 255, 255))
            screen.blit(text,(1000,770))
            text = font.render('Actions: '+str(["{:0.2f}".format(x) for x in action[0]]), True, (255, 255, 255))
            screen.blit(text,(100,700))
            trget = action.copy()
            taction = ag.gettrainaction(np.array([t.x-cars[0].pos.x,t.y-cars[0].pos.y,cars[0].vel.x,cars[0].vel.y,cars[0].heading.x,cars[0].heading.y,cars[0].pos.x,cars[0].pos.y]).reshape((1,-1)))
            trget[0][np.argmax(action[0])] = cars[0].reward + ag.discount*taction[0][np.argmax(action[0])]
            text = font.render('Taction: '+str(["{:0.2f}".format(x) for x in taction[0]]), True, (255, 255, 255))
            screen.blit(text,(100,720))
            text = font.render('Target: '+str(["{:0.2f}".format(x) for x in trget[0]]), True, (255, 255, 255))
            screen.blit(text,(100,740))
            text = font.render('Episode: '+ str(ag.episode) + "  Iteration: " + str(ag.count), True, (255, 255, 255))
            screen.blit(text,(100,760))
        else:
            pygame.draw.rect(screen,(255,255,255),cars[0].hitbox,4)
        if(frame<=secondstorecord*120 and frame%6==0):
            recorder.capture_frame(screen)
        pygame.display.flip()

    frame+=1

    if(pygame.key.get_pressed()[pygame.K_ESCAPE] and not saved):
        recorder.end_recording()
        print("Recording saved")
        saved = True

    if AI:
        # ag.storeexp(state,action,cars[0].reward,np.array([cars[0].pos.x/1280,cars[0].pos.y/700,cars[0].vel.x/520,cars[0].vel.y/520,t.x/1280,t.y/700]).reshape((1,-1)))
        ag.storeexp(state,action,cars[0].reward,np.array([t.x-cars[0].pos.x,t.y-cars[0].pos.y,cars[0].vel.x,cars[0].vel.y,cars[0].heading.x,cars[0].heading.y,cars[0].pos.x,cars[0].pos.y]).reshape((1,-1)))

    
    
