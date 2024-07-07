import pygame
import random
import math
from Car import Car
from Wall import Wall
from Ball import Ball

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

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
# cars.append(Car((800,300)))

walls = []
walls.append(Wall((10,10),(1250,20),pygame.Vector2(0,1)))
walls.append(Wall((10,670),(1250,20),pygame.Vector2(0,1)))
walls.append(Wall((10,10),(20,680),pygame.Vector2(1,0)))
walls.append(Wall((1250,10),(20,680),pygame.Vector2(1,0)))

# b = Ball((635,345))

g = Goal((1250,267),(20,165))

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
            car.reward += 500


t = target(500,500)
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

while running:
    cars[0].reward =-1
    cars[0].reward +=  math.exp(-(((cars[0].pos - pygame.Vector2(t.x,t.y)).length())/300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    wpressed = keys[pygame.K_w]
    apressed = keys[pygame.K_a]
    spressed = keys[pygame.K_s]
    dpressed = keys[pygame.K_d]


    screen.fill((0,0,0))
    dt = clock.tick(120) / 1000

    cars[0].tick(dt,wpressed,spressed,dpressed,apressed)
    for c in cars:
        c.render(screen)
    for w in walls:
        w.render(screen)
        for c in cars:
            w.collision(c,dt)

    t.render(screen)
    t.collision(cars[0])

    text = font.render('Score: '+str(cars[0].score), True, (255, 255, 255))
    screen.blit(text,(1000,50))
    text = font.render('Reward: '+str(cars[0].reward), True, (255, 255, 255))
    screen.blit(text,(1000,100))

    cars[0].score += cars[0].reward*0.01
    g.render(screen)
    # g.collision(b)
    # pygame.draw.rect(screen,(255,0,0),cars[0].hitbox,2)
    # pygame.draw.rect(screen,(255,0,0),b.hitbox,2)
    pygame.display.flip()
    
