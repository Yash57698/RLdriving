import pygame
from Car import Car
from Wall import Wall
from Ball import Ball

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

c = Car((300,300))

walls = []
walls.append(Wall((10,10),(1250,20),pygame.Vector2(0,1)))
walls.append(Wall((10,670),(1250,20),pygame.Vector2(0,1)))
walls.append(Wall((10,10),(20,680),pygame.Vector2(1,0)))
walls.append(Wall((1250,10),(20,680),pygame.Vector2(1,0)))

b = Ball((500,500))

wpressed = False
apressed = False
spressed = False
dpressed = False

while running:
    
    
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
    # print(dt)
    # dt = 0.017
    c.tick(dt,wpressed,spressed,dpressed,apressed)
    c.render(screen)
    for w in walls:
        w.render(screen)
        w.collision(c)
        w.ballcollision(b)

    b.render(screen)
    b.tick(dt)
    b.collision(c)
    # pygame.draw.rect(screen,(255,0,0),c.hitbox,2)
    # pygame.draw.rect(screen,(255,0,0),b.hitbox,2)
    pygame.display.flip()
    
