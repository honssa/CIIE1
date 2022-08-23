import pygame
import os
import math
from observers.EnemyDeathObserver import EnemyDeathObserver

class Target(EnemyDeathObserver):
    def __init__(self,target):
        self.enemy = target
    def notificar(self,obj):
        self.enemy = None

class Projectile(pygame.sprite.Sprite):
    def __init__(self,X,Y,delay,target,damage):
        self.X = X
        self.Y = Y
        self.delay = delay
        self.progress = 0
        self.dmg = damage
        self.target = Target(target)

        self.actualX = self.X
        self.actualY = self.Y

        self.image = pygame.image.load(os.path.join("Assets", "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self, window, camera):
        #Formula de punto medio con porcentaje: p1 + (p2-p1) * percentage

        self.actualX = self.X + (self.target.enemy.X - self.X) * (self.progress/self.delay)
        self.actualY = self.Y + (self.target.enemy.Y - self.Y) * (self.progress/self.delay)

        self.rect.centerx = self.actualX + camera.X
        self.rect.centery = self.actualY + camera.Y
   
        angle = math.atan2(self.Y - self.target.enemy.Y, self.X - self.target.enemy.X) * 180 / math.pi
        window.blit(pygame.transform.rotate(self.image, -angle), self.rect)


    def update(self):
        if (self.target.enemy == None):
            return False

        self.progress += 1
        if (self.progress == self.delay):
            self.target.enemy.hit(self.dmg)
            return False
        return True



class ArtilleryProjectile(Projectile):
    def __init__(self, X,Y, delay, target, damage, enemies_radius=[], area_dmg=0):
        self.X = X
        self.Y = Y
        self.delay = delay
        self.progress = 0
        self.enemies_radius = enemies_radius
        self.dmg = damage
        self.area_dmg = area_dmg
        self.target = Target(target)
        self.image = pygame.image.load(os.path.join("Assets", "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        if (self.target.enemy == None):
            return False

        self.progress += 1
        if (self.progress == self.delay):
            self.target.enemy.hit(self.dmg)
            for enemy in self.enemies_radius:
                enemy.hit(self.area_dmg)
            return False
        return True

