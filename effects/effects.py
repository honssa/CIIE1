import pygame
import os

def divide_imagen(image, rect):
    subimage = image.subsurface(rect)
    return subimage, rect



class BombExplosion:
    # Pattern e unha lista de listas de tuplas de coordenadas (x,y) do mundo onde estara situada cada explosion
    # stime e o intervalo de tempo entre cada elemento de pattern
    def __init__(self, pattern, stime):
        self.explosionImage = pygame.image.load(os.path.join("Assets/sprites/effects/", "explosion-1.png")).convert_alpha()
        self.explosionImages = []
        self.pattern = pattern
        self.stime = stime
        self.pattern_index = 1  # Contador
        self.tam_sprite = (32,32)
        self.sprite_count = 0
        self.general_count = 0
        self.offset_sprite = (-16, -16)
        self.active_animations = []
        self.podese_borrar = False

        for element in self.pattern:
            self.active_animations.append(0)
        self.active_animations[0] = 1

        for x in range(0, self.explosionImage.get_width(), 32):
            subimage, rect = divide_imagen(self.explosionImage, pygame.Rect((x,0) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.explosionImages.append(subimage)


    def draw(self, window, camera, grid):
        if ( self.pattern_index * 12 == self.general_count) and ( len(self.pattern) > (self.pattern_index) ):
            self.active_animations[self.pattern_index] = 1
            self.pattern_index += 1

        
        # Todas as explosions no momento
        for i in range(len(self.active_animations)):
            if self.active_animations[i] > 0:
                if (self.active_animations[i]-1) >= len(self.explosionImages) * 3:
                    self.active_animations[i] = 0
                    break
                for pos in self.pattern[i]:
                    wpos = grid.map_to_world(pos)
                    current_sprite = self.explosionImages[(self.active_animations[i]-1) // 3]
                    window.blit(current_sprite, ((wpos[0] + camera.X + self.offset_sprite[0]), (wpos[1] + camera.Y + self.offset_sprite[1])) )
                self.active_animations[i] += 1

        # despois de debuxar, incrementar o contador xeneral
        self.general_count += 1



class ScissorsExplosion():
    def __init__(self, x, y):
        self.explosionImage = pygame.image.load(os.path.join("Assets/sprites/effects/", "scissors_effect.png")).convert_alpha()
        self.explosionImages = []
        self.X = x
        self.Y = y
        self.tam_sprite = (200,200)
        self.sprite_count = 0
        self.offset_sprite = (-100, -100)
        self.podese_borrar = False

        print(str(self.explosionImage.get_width()) + " , " + str(self.explosionImage.get_height()))
        for y in range(0, self.explosionImage.get_height(), 200):
            for x in range(0, self.explosionImage.get_width(), 200):
                subimage, rect = divide_imagen(self.explosionImage, pygame.Rect((x,y) ,self.tam_sprite) )
                self.explosionImages.append(subimage)
            


    def draw(self, window, camera, grid):
        self.sprite_count += 1
        if self.sprite_count < len(self.explosionImages) * 3: 
            current_sprite = self.explosionImages[self.sprite_count // 3]
            window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        else:
            self.podese_borrar = True




class PaperInterference():
    def __init__(self, x, y):
        self.interferenceImage = pygame.image.load(os.path.join("Assets/sprites/effects/", "paper_effect.png")).convert_alpha()
        self.preparacionImages = []
        self.attackImages = []
        self.X = x
        self.Y = y
        self.tam_sprite = (416,416)
        self.sprite_count = 0
        self.offset_sprite = (-208, -208)
        self.podese_borrar = False
        self.current_animation = "preparacion"
        self.loops = 0

        for x in range(0, self.interferenceImage.get_width(), self.tam_sprite[0]):
            subimage, rect = divide_imagen(self.interferenceImage, pygame.Rect((x,0) ,self.tam_sprite) )
            self.preparacionImages.append(subimage)
        
        for x in range(0, self.tam_sprite[0]*4, self.tam_sprite[0]):
            subimage, rect = divide_imagen(self.interferenceImage, pygame.Rect((x,self.tam_sprite[1]) ,self.tam_sprite) )
            self.attackImages.append(subimage)

            


    def draw(self, window, camera, grid):
        self.sprite_count += 1
        if self.current_animation == "preparacion":
            if self.sprite_count < len(self.preparacionImages) * 3: #100 ms frecuencia
                current_sprite = self.preparacionImages[self.sprite_count // 3]
                window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
            else:
                self.current_animation = "attack"
                self.sprite_count = 0
        elif self.current_animation == "attack":
            if self.loops >= 5:
                self.podese_borrar = True
            elif self.sprite_count < len(self.attackImages) * 6: #100 ms frecuencia
                current_sprite = self.attackImages[self.sprite_count // 6]
                window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
            else:
                self.sprite_count = 0
                self.loops += 1
                return "i_hit"