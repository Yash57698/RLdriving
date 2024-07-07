import pygame

class Ball:
    restitution = 2
    deaccfactor = 0.99
    maxvel = 600

    def __init__(self,pos = (500,500)):
        self.pos = pos
        self.vel = pygame.Vector2(-1000,0)
        self.image = pygame.image.load("C:/Users/yashs/Desktop/Project/RLdriving/kenney_racing-pack/PNG/Objects/barrel_blue.png")
        self.massratio = 0.1

    def tick(self,dt):
        self.vel = self.vel * self.deaccfactor
        if(self.vel.length() > 0.1):
            self.vel = self.vel.normalize() * min(self.vel.length(),self.maxvel)
        self.pos += self.vel * dt
    
    def render(self,screen):
        screen.blit(self.image,self.pos)
        self.hitbox = (self.image).get_rect(topleft = self.pos)

    def collision(self,car):
        if pygame.Rect(self.pos,(self.image.get_width(),self.image.get_height())).colliderect(car.hitbox):
            vcar = car.vel - (((2/(1+(1/self.massratio))) * (car.vel - self.vel).dot(pygame.Vector2(car.hitbox.center) - self.hitbox.center) / (pygame.Vector2(car.hitbox.center) - self.hitbox.center).length_squared()))* (pygame.Vector2(car.hitbox.center) - self.hitbox.center)
            vball = self.vel - (((2/(1+self.massratio)) * (self.vel - car.vel).dot(pygame.Vector2(self.hitbox.center) - car.hitbox.center) / (pygame.Vector2(self.hitbox.center) - car.hitbox.center).length_squared()))* (pygame.Vector2(self.hitbox.center) - car.hitbox.center)
            # car.heading = vcar.normalize()
            # print(vcar,car.vel,car.speed,vcar.length())
            car.vel = vcar
            
            car.speed = vcar.dot(car.heading)
            self.vel = vball