import pygame

class Car:
    acc = 1000
    turnacc = 150
    maxvel = 500
    deaccfactor = 0.99

    def __init__(self,pos = (0,0)):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0,0.1)
        self.heading = pygame.Vector2(0,1)
        self.image =  pygame.transform.scale_by(pygame.image.load("./kenney_racing-pack/PNG/Cars/car_black_1.png"),0.4)
        self.speed =0 
        self.hitbox = pygame.transform.rotate(self.image,pygame.Vector2.angle_to(self.heading,(0,1))).get_rect(topleft = self.pos)
        self.lastrotation = 0
        self.score = 0
        self.reward =0

    def tick(self,dt,inputup = False,inputdown = False,inputright = False,inputleft = False):
        
        self.laststate = (self.pos,self.vel,self.heading,self.speed)
        
        self.speed = self.speed * self.deaccfactor
        
        if inputup or inputdown:
            if inputleft or inputright:
                self.vel = self.vel - self.vel.dot(self.heading) * self.heading
                self.vel = self.vel * 0.7
            self.speed += self.acc * dt * -(inputup-inputdown)
            self.speed = max(-self.maxvel,min(self.speed,self.maxvel))

        self.vel = self.vel - self.vel.dot(self.heading) * self.heading
        self.vel = self.vel * 0.95
        self.vel = self.heading * self.speed + self.vel
        self.pos += self.vel * dt

        if inputup:
            self.heading = self.heading.rotate(-(inputleft-inputright)*self.turnacc*dt)
        if inputdown:
            self.heading = self.heading.rotate((inputleft-inputright)*self.turnacc*dt)
        self.speed = self.vel.dot(self.heading)
        

    def render(self,screen):
        screen.blit(pygame.transform.rotate(self.image,pygame.Vector2.angle_to(self.heading,(0,1))),self.pos)
        self.hitbox = pygame.transform.rotate(self.image,pygame.Vector2.angle_to(self.heading,(0,1))).get_rect(topleft = self.pos)