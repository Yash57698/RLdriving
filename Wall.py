import pygame

class Wall:
    def __init__(self, pos, size,normal):
        self.rect = pygame.Rect(pos, size)
        self.color = (255, 255, 255)
        self.normal = normal

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collision(self, car,dt):
        if self.rect.colliderect(car.hitbox):
            
            
            car.heading = car.heading.rotate(-car.lastrotation)
            car.pos -= 2*(abs(car.vel.dot(self.normal))*self.normal) * dt
            
            vcar = car.vel - (2 * (car.vel.dot(self.normal))*self.normal)
            car.vel = vcar
            car.speed = vcar.dot(car.heading)
        

    def ballcollision(self,ball,dt):
        if self.rect.colliderect(pygame.Rect(ball.pos,(ball.image.get_width(),ball.image.get_height()))):
            ball.pos = ball.pos
            ball.pos -= (ball.vel.dot(self.normal)*self.normal) * dt
            ball.vel = ball.vel.reflect(self.normal)