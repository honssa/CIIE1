import pygame
import os
import math

class Gate(pygame.sprite.Sprite):
    #def __init__(self,grid,X,Y):
    def __init__(self,grid,orientacion,pos):
        self.orientacion = orientacion

        if self.orientacion == "horizontal":
            # Imaxes da porta horizontal
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets/gate", "gate0.png")).convert_alpha(),(grid.tileSize[0]*2,grid.tileSize[1]*4))
            self.image2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets/gate", "gate1.png")).convert_alpha(),(grid.tileSize[0]*4,grid.tileSize[1]*4))
            self.image3 = pygame.transform.flip(self.image2,True,False)
            self.pos = (pos,(pos[0]-1,pos[1]),(pos[0]+1,pos[1]))

        elif self.orientacion == "vertical":
            # Imaxes da porta vertical
            self.image = pygame.image.load(os.path.join("Assets/gate", "gate0_vertical.png")).convert_alpha()
            self.image2 = pygame.image.load(os.path.join("Assets/gate", "gate1_vertical.png")).convert_alpha()
            self.image3 = pygame.image.load(os.path.join("Assets/gate", "gate2_vertical.png")).convert_alpha()
            self.pos = ((pos[0],pos[1]-2),(pos[0],pos[1]-3),(pos[0],pos[1]-1))

        self.rect = self.image.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect3 = self.image3.get_rect()
        self.X = (pos[0]-0.5)*grid.tileSize[0]
        self.Y = (pos[1]-3)*grid.tileSize[1]

        self.health = 100

    def draw(self, window, camera):
        self.rect.x = self.X + camera.X
        self.rect.y = self.Y + camera.Y
        if self.orientacion == "horizontal":
            self.rect2.x = self.rect.x + self.rect.width
            self.rect2.y = self.rect.y
            self.rect3.x = self.rect.x - self.rect3.width
            self.rect3.y = self.rect.y
        elif self.orientacion == "vertical":
            self.rect2.x = self.rect.x
            self.rect2.y = self.rect.y + self.rect2.height
            self.rect3.x = self.rect.x
            self.rect3.y = self.rect.y - self.rect3.height
        window.blit(self.image, self.rect)
        window.blit(self.image2,self.rect2)
        window.blit(self.image3,self.rect3)

