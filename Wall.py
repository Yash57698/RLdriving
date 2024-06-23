import pygame

class Wall:
    def __init__(self, pos, size,normal):
        self.rect = pygame.Rect(pos, size)
        self.color = (255, 255, 255)
        self.normal = normal

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collision(self, car):
        if self.rect.colliderect(car.hitbox):
            vcar = car.vel - (2 * (car.vel.dot(self.normal))*self.normal)
            
            # car.speed = vcar.length()
            # if(vcar.dot(car.vel) < 0):
            car.speed = -car.speed
            # car.heading = vcar.normalize()

    def ballcollision(self,ball):
        if self.rect.colliderect(pygame.Rect(ball.pos,(ball.image.get_width(),ball.image.get_height()))):
            ball.pos = ball.pos
            ball.vel = ball.vel.reflect(self.normal)