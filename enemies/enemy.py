import pygame
import os


class EnemySubject():    #Parte del Patron Observador
    def __init__(self):
        self.observadores = []
    def onEnemyDeath(self,enemy):
        for o in self.observadores:
            o.notificar(enemy)

    def attach(self,o):
        self.observadores.append(o)

    def detach(self,o):
        self.observadores.remove(o)


# Colle unha parte da imaxe 
def divide_imagen(image, rect):
    subimage = image.subsurface(rect)
    return subimage, rect

class Enemy(pygame.sprite.Sprite):

    def __init__(self,path,grid):
        # Invocamos ao constructor da clase pai
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Assets", "enemy.png")).convert_alpha()
        self.imageEnemyBomb = pygame.image.load(os.path.join("Assets", "enemy_bomb.png")).convert_alpha()


        # Posicion do sprite
        self.rect = self.image.get_rect()
        self.path = path
        self.segment = 0 # indice do segmento do percorrido
        world_pos = grid.map_to_world((path[0]["ini"][0], path[0]["ini"][1])) 
        self.X = world_pos[0]
        self.Y = world_pos[1]

        self.rect.centerx = self.X
        self.rect.centery = self.Y
        self.name = 'basic'

        # Cousas dos sprites
        self.current_animation = "run"
        self.offset_sprite = (-54, -123)
        self.sprite_count = 0
        self.enemy_0_run_imgs = []
        self.enemy_0_hit_imgs = []
        self.enemy_0_death_imgs = []
        self.enemy_0_sprite_run_img = pygame.image.load(os.path.join("Assets/sprites", "enemy_0_run.png")).convert_alpha()
        self.enemy_0_sprite_hit_img = pygame.image.load(os.path.join("Assets/sprites", "enemy_0_hit.png")).convert_alpha()
        self.enemy_0_sprite_death_img = pygame.image.load(os.path.join("Assets/sprites", "enemy_0_death.png")).convert_alpha()
        self.tam_sprite = (112,124)
        for x in range(0, self.enemy_0_sprite_run_img.get_height(), 124):
            subimage, rect = divide_imagen(self.enemy_0_sprite_run_img, pygame.Rect((0,x+1) ,(self.tam_sprite[0],self.tam_sprite[1]-1) ))
            self.enemy_0_run_imgs.append(subimage)
        
        for x in range(0, self.enemy_0_sprite_hit_img.get_height(), 124):
            subimage, rect = divide_imagen(self.enemy_0_sprite_hit_img, pygame.Rect((0,x+1) ,(self.tam_sprite[0],self.tam_sprite[1]-1) ))
            self.enemy_0_hit_imgs.append(subimage)
        
        for x in range(0, self.enemy_0_sprite_death_img.get_height(), 124):
            subimage, rect = divide_imagen(self.enemy_0_sprite_death_img, pygame.Rect((0,x+1) ,(self.tam_sprite[0],self.tam_sprite[1]-1) ))
            self.enemy_0_death_imgs.append(subimage)

        # Resto de atributos
        self.vel = 1.5    # velocidade
        self.max_health = 30
        self.health = 30
        self.chatarra = 1

        self.killed = False


        self.subject = EnemySubject()

    def attachObserver(self,o):
        self.subject.attach(o)
    def detachObserver(self,o):
        self.subject.detach(o)

    def draw(self, window, camera):
        if self.current_animation == "run":
            self.sprite_count += 1
            if self.sprite_count >= len(self.enemy_0_run_imgs) * 6:
                self.sprite_count = 0
            current_sprite = self.enemy_0_run_imgs[self.sprite_count // 6]
            window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        elif self.current_animation == "hit":
            self.sprite_count += 1
            if self.sprite_count >= len(self.enemy_0_hit_imgs) * 6:
                self.sprite_count = 0
                self.current_animation = "run"
            current_sprite = self.enemy_0_hit_imgs[self.sprite_count // 6]
            window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        elif self.current_animation == "death":
            self.sprite_count += 1
            if self.sprite_count >= len(self.enemy_0_death_imgs) * 6:
                self.sprite_count = 0
                self.subject.onEnemyDeath(self)
                return None
            current_sprite = self.enemy_0_death_imgs[self.sprite_count // 6]
            window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )

        self.draw_health_bar(window, camera)


    def draw_health_bar(self, window, camera):
        if not (self.health < self.max_health):
            return None
        length = 30

        move_by = self.health / self.max_health

        health_bar = round(length * move_by)

        offset_x = -15
        offset_y = -40

        pygame.draw.rect(window, (44, 54, 52), (self.X+offset_x+camera.X, self.Y+offset_y+camera.Y, length, 5), 0)
        pygame.draw.rect(window, (191,228,230), (self.X+offset_x+camera.X, self.Y+offset_y+camera.Y, health_bar, 5), 0)


    def move(self, grid):
        world_pos = grid.map_to_world(self.path[self.segment]["fin"])

        # Se esta cerca
        map_pos = grid.world_to_map((self.X, self.Y))
        if grid.is_barricade(map_pos):
            return
        if map_pos == self.path[self.segment]["fin"]:

            if self.segment == len(self.path)-1: # Recorrido remata
                self.subject.onEnemyDeath(self)
                return
            else:
                self.segment += 1
                self.X = world_pos[0]; self.Y = world_pos[1]

        direction = self.path[self.segment]["dir"]
        self.X += direction[0]*self.vel
        self.Y += direction[1]*self.vel

    def checkForGate(self,gate,grid):
        world_pos = grid.world_to_map((self.X,self.Y))
        #gatesound2 = pygame.mixer.Sound("Sounds/metal_interaction2.wav")
        if (world_pos in gate.pos):
            self.chatarra = 0   #Se morren pola porta non dan chatarra
            pygame.mixer.Sound("Sounds/novos/wall_hit_qubodup.ogg").play()
            #gatesound2.play()
            self.subject.onEnemyDeath(self)
            world_pos = None
            return True 
        return False
            

    def collide(self, target_sprite):
        # verifica se impacata contra outro sprite
        return self.rect.colliderect(target_sprite.rect)

    def hit(self, dmg):
        self.health -= dmg
        if (self.health <= 0 and not self.killed):
            if self.name == "basic":
                basic_sound =pygame.mixer.Sound("Sounds/novos/robot_dead_remaxim.ogg")
                basic_sound.set_volume(0.2)
                basic_sound.play()
            elif self.name == "veloz":
                pygame.mixer.Sound("Sounds/novos/veloz_death_michelbaradari.ogg").play()
            elif self.name == "tanque":
                pygame.mixer.Sound("Sounds/novos/tank_death_bertsz.ogg").play()
            elif self.name == "bomba":
                pygame.mixer.Sound("Sounds/novos/bomb_dead_Luke.RUSTLTD.ogg").play()
            elif self.name == "enxenheiro":
                pygame.mixer.Sound("Sounds/novos/robot_dead_remaxim.ogg").play()
            #death_sound = pygame.mixer.Sound("Sounds/impactsplat04.mp3.flac").play()
            self.killed = True
            self.subject.onEnemyDeath(self)
            return True
        if not (self.current_animation == "ability"):
            self.current_animation = "hit"
            self.sprite_count = 0
        return False
    

    def ability(self, enemies, grid):
        pass
    
    # Metodo para as torres de dano acumulativo
    #def reg_rad_accu()




class EnemyDead(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        self.enemy_0_death_imgs = []
        self.enemy_0_sprite_death_img = pygame.image.load(os.path.join("Assets/sprites", "enemy_0_death.png")).convert_alpha()
        self.tam_sprite = (112,124)
        self.sprite_count = 0
        self.name = 'basic'
        self.X = X
        self.Y = Y
        self.offset_sprite = (-54, -123)
        for x in range(0, self.enemy_0_sprite_death_img.get_height(), 124):
            subimage, rect = divide_imagen(self.enemy_0_sprite_death_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]-1) ))
            self.enemy_0_death_imgs.append(subimage)


    def draw(self, window, camera): 
        delete = False
        self.sprite_count += 1
        if self.sprite_count >= len(self.enemy_0_death_imgs) * 6:
            self.sprite_count = 0
            delete = True

            return delete
        current_sprite = self.enemy_0_death_imgs[self.sprite_count // 6]
        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        return delete


class EnemyVelozDead(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        self.enemy_1_death_imgs = []
        self.enemy_1_sprite_death_img = pygame.image.load(os.path.join("Assets/sprites/enemy_veloz", "enemy_1_death.png")).convert_alpha()
        self.tam_sprite = (106,22)
        self.sprite_count = 0
        self.name = 'veloz'
        self.X = X
        self.Y = Y
        self.offset_sprite = (-26, -12)
        for x in range(0, self.enemy_1_sprite_death_img.get_width(), 106):
            subimage, rect = divide_imagen(self.enemy_1_sprite_death_img, pygame.Rect((x,0) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_1_death_imgs.append(subimage)


    def draw(self, window, camera): 
        delete = False
        self.sprite_count += 1
        if self.sprite_count >= len(self.enemy_1_death_imgs) * 6:
            self.sprite_count = 0
            delete = True
            return delete
        current_sprite = pygame.transform.scale(self.enemy_1_death_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        return delete



class EnemyTankDead(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        self.enemy_2_death_imgs = []
        self.enemy_2_sprite_death_img = pygame.image.load(os.path.join("Assets/sprites/enemy_tank", "enemy_2_death.png")).convert_alpha()
        self.tam_sprite = (96,96)
        self.sprite_count = 0
        self.name = 'tanque'
        self.X = X
        self.Y = Y
        self.offset_sprite = (-56, -48)
        for x in range(0, self.enemy_2_sprite_death_img.get_width(), 96):
            subimage, rect = divide_imagen(self.enemy_2_sprite_death_img, pygame.Rect((x,0) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_2_death_imgs.append(subimage)


    def draw(self, window, camera): 
        delete = False
        self.sprite_count += 1
        if self.sprite_count >= len(self.enemy_2_death_imgs) * 6:
            self.sprite_count = 0
            delete = True
            return delete
        current_sprite = self.enemy_2_death_imgs[self.sprite_count // 6]
        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        return delete


class EnemyBombDead(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        self.enemy_3_death_imgs = []
        self.enemy_3_sprite_death_img = pygame.image.load(os.path.join("Assets/sprites/enemy_bomb", "enemy_3_death.png")).convert_alpha()
        self.tam_sprite = (90,32)
        self.sprite_count = 0
        self.name = 'bomba'
        self.X = X
        self.Y = Y
        self.offset_sprite = (-45, -16)
        for x in range(0, self.enemy_3_sprite_death_img.get_width(), 32):
            subimage, rect = divide_imagen(self.enemy_3_sprite_death_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_3_death_imgs.append(subimage)


    def draw(self, window, camera): 
        delete = False
        self.sprite_count += 1
        if self.sprite_count >= len(self.enemy_3_death_imgs) * 6:
            self.sprite_count = 0
            delete = True
            return delete
        current_sprite = self.enemy_3_death_imgs[self.sprite_count // 6]
        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        return delete




class EnemyEngeneerDead(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        self.enemy_4_death_imgs = []
        self.enemy_4_sprite_death_img = pygame.image.load(os.path.join("Assets/sprites/enemy_enxenheiro", "enemy_4_death.png")).convert_alpha()
        self.tam_sprite = (36,39)
        self.sprite_count = 0
        self.name = 'enxenheiro'
        self.X = X
        self.Y = Y
        self.offset_sprite = (-36, -46)
        for x in range(0, self.enemy_4_sprite_death_img.get_height(), 39):
            subimage, rect = divide_imagen(self.enemy_4_sprite_death_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_4_death_imgs.append(subimage)


    def draw(self, window, camera): 
        delete = False
        self.sprite_count += 1
        if self.sprite_count >= len(self.enemy_4_death_imgs) * 6:
            self.sprite_count = 0
            delete = True
            return delete
        current_sprite = pygame.transform.scale(self.enemy_4_death_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0]), (self.Y + camera.Y + self.offset_sprite[1])) )
        return delete










class EnemyEngeneer(Enemy):
    def __init__(self,path,grid):
        self.vel = 0.8
        self.max_health = 50
        self.health = 50
        self.chatarra = 5
        self.subject = EnemySubject()
        self.killed = False

        self.path = path
        self.segment = 0 # indice do segmento do percorrido
        world_pos = grid.map_to_world((path[0]["ini"][0], path[0]["ini"][1])) 
        self.X = world_pos[0]
        self.Y = world_pos[1]

        self.ability_counter = 0 # Contador para facer a abilidade
        self.recharge_time = 360 #(6*60) -> 6 segundos
        self.ability_range = 4


        # Cousas dos sprites
        self.current_animation = "run"
        self.offset_sprite = (-36, -46)
        self.sprite_count = 0

        self.name = 'enxenheiro'

        self.enemy_4_run_imgs = []
        self.enemy_4_run2_imgs = []
        self.enemy_4_hit_imgs = []
        self.enemy_4_hit2_imgs = []
        self.enemy_4_ability_imgs = []
        self.enemy_4_ability2_imgs = []
        self.enemy_4_sprite_run_img = pygame.image.load(os.path.join("Assets/sprites/enemy_enxenheiro", "enemy_4_run.png")).convert_alpha()
        self.enemy_4_sprite_hit_img = pygame.image.load(os.path.join("Assets/sprites/enemy_enxenheiro", "enemy_4_hit.png")).convert_alpha()
        self.enemy_4_sprite_ability_img = pygame.image.load(os.path.join("Assets/sprites/enemy_enxenheiro", "enemy_4_charge.png")).convert_alpha()
        self.tam_sprite = (36,39)
        for x in range(0, self.enemy_4_sprite_run_img.get_height(), 39):
            subimage, rect = divide_imagen(self.enemy_4_sprite_run_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_4_run_imgs.append(subimage)
            self.enemy_4_run2_imgs.append(pygame.transform.flip(subimage,True,False))
        
        for x in range(0, self.enemy_4_sprite_hit_img.get_height(), 39):
            subimage, rect = divide_imagen(self.enemy_4_sprite_hit_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_4_hit_imgs.append(subimage)
            self.enemy_4_hit2_imgs.append(pygame.transform.flip(subimage,True,False))
        
        for x in range(0, self.enemy_4_sprite_ability_img.get_height(), 39):
            subimage, rect = divide_imagen(self.enemy_4_sprite_ability_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_4_ability_imgs.append(subimage)
            self.enemy_4_ability2_imgs.append(pygame.transform.flip(subimage,True,False))
        


    def draw(self, window, camera):
        extra_offset = 0
        direction = self.path[self.segment]["dir"]
        if self.current_animation == "run":
            self.sprite_count += 1
            if direction == (-1,0):
                if self.sprite_count >= len(self.enemy_4_run2_imgs) * 6:
                    self.sprite_count = 0
                current_sprite = pygame.transform.scale(self.enemy_4_run2_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
                extra_offset = 0 

            else:
                if self.sprite_count >= len(self.enemy_4_run_imgs) * 6:
                    self.sprite_count = 0
                current_sprite = pygame.transform.scale(self.enemy_4_run_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))

    
        elif self.current_animation == "hit":
            self.sprite_count += 1

            if direction == (-1,0):
                if self.sprite_count >= len(self.enemy_4_hit2_imgs) * 6:
                    self.sprite_count = 0
                    self.current_animation = "run"
                current_sprite = pygame.transform.scale(self.enemy_4_hit2_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
                extra_offset = 0 

            else:
                if self.sprite_count >= len(self.enemy_4_hit_imgs) * 6:
                    self.sprite_count = 0
                    self.current_animation = "run"
                current_sprite = pygame.transform.scale(self.enemy_4_hit_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
        
        elif self.current_animation == "ability":
            self.sprite_count += 1

            if direction == (-1,0):
                if self.sprite_count >= len(self.enemy_4_ability2_imgs) * 6:
                    self.sprite_count = 0

                current_sprite = pygame.transform.scale(self.enemy_4_ability2_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
                extra_offset = 0

            else:
                if self.sprite_count >= len(self.enemy_4_ability_imgs) * 6:
                    self.sprite_count = 0

                current_sprite = pygame.transform.scale(self.enemy_4_ability_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))

        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0] + extra_offset), (self.Y + camera.Y + self.offset_sprite[1])) )
        self.draw_health_bar(window, camera)
    

    # Cura aos enemigos
    def ability(self, enemies, grid):
        self.ability_counter += 1
        if (self.ability_counter >= self.recharge_time + 144):  # Para de executar a abilidade
            self.current_animation = "run"
            self.ability_counter = 0
        elif (self.ability_counter >= self.recharge_time) and ((self.ability_counter % 8) == 0):
            if self.current_animation != "ability":
                self.current_animation = "ability"
            map_pos = grid.world_to_map((self.X, self.Y))
            cells = grid.get_range_cells(map_pos, self.ability_range)
            for enemy in enemies.list:
                enemy_pos = grid.world_to_map((enemy.X,enemy.Y))
                if grid.is_2_area_intersecting(cells, [enemy_pos]):
                    if enemy.health < enemy.max_health:
                        enemy.health += 1












class EnemyBomb(Enemy):
    def __init__(self,path,grid):
        self.vel = 2
        self.max_health = 20
        self.health = 20
        self.chatarra = 0
        self.subject = EnemySubject()
        self.killed = False

        self.path = path
        self.segment = 0 # indice do segmento do percorrido
        world_pos = grid.map_to_world((path[0]["ini"][0], path[0]["ini"][1])) 
        self.X = world_pos[0]
        self.Y = world_pos[1]

        # Cousas dos sprites
        self.current_animation = "run"
        self.offset_sprite = (-45, -16)
        self.sprite_count = 0

        self.name = 'bomba'

        self.enemy_3_run_imgs = []
        self.enemy_3_hit_imgs = []
        self.enemy_3_sprite_run_img = pygame.image.load(os.path.join("Assets/sprites/enemy_bomb", "enemy_3_run.png")).convert_alpha()
        self.enemy_3_sprite_hit_img = pygame.image.load(os.path.join("Assets/sprites/enemy_bomb", "enemy_3_hit.png")).convert_alpha()
        self.tam_sprite = (90,32)
        for x in range(0, self.enemy_3_sprite_run_img.get_height(), 32):
            subimage, rect = divide_imagen(self.enemy_3_sprite_run_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_3_run_imgs.append(subimage)
        
        for x in range(0, self.enemy_3_sprite_hit_img.get_height(), 32):
            subimage, rect = divide_imagen(self.enemy_3_sprite_hit_img, pygame.Rect((0,x) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_3_hit_imgs.append(subimage)

        

    def draw(self, window, camera):
        extra_offset = 0
        if self.current_animation == "run":
            self.sprite_count += 1
            if self.sprite_count >= len(self.enemy_3_run_imgs) * 6:
                self.sprite_count = 0
            current_sprite = self.enemy_3_run_imgs[self.sprite_count // 6]

    
        elif self.current_animation == "hit":
            self.sprite_count += 1
            if self.sprite_count >= len(self.enemy_3_hit_imgs) * 6:
                self.sprite_count = 0
                self.current_animation = "run"
            current_sprite = self.enemy_3_hit_imgs[self.sprite_count // 6]

        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0] + extra_offset), (self.Y + camera.Y + self.offset_sprite[1])) )
        self.draw_health_bar(window, camera)




class EnemyVeloz(Enemy):
    def __init__(self,path,grid):
        self.vel = 4
        self.max_health = 12
        self.health = 12
        self.chatarra = 2
        self.subject = EnemySubject()
        self.killed = False

        self.path = path
        self.segment = 0 # indice do segmento do percorrido
        world_pos = grid.map_to_world((path[0]["ini"][0], path[0]["ini"][1])) 
        self.X = world_pos[0]
        self.Y = world_pos[1]

        # Cousas dos sprites
        self.current_animation = "run"
        self.offset_sprite = (-26, -12)
        self.sprite_count = 0

        self.name = 'veloz'

        self.enemy_1_run_imgs = []
        self.enemy_1_run2_imgs = []
        self.enemy_1_hit_imgs = []
        self.enemy_1_hit2_imgs = []
        self.enemy_1_death_imgs = []
        self.enemy_1_sprite_run_img = pygame.image.load(os.path.join("Assets/sprites/enemy_veloz", "enemy_1_run.png")).convert_alpha()
        self.enemy_1_sprite_hit_img = pygame.image.load(os.path.join("Assets/sprites/enemy_veloz", "enemy_1_hit.png")).convert_alpha()
        self.enemy_1_sprite_death_img = pygame.image.load(os.path.join("Assets/sprites/enemy_veloz", "enemy_1_death.png")).convert_alpha()
        self.tam_sprite = (106,22)
        for x in range(0, self.enemy_1_sprite_run_img.get_width(), 106):
            subimage, rect = divide_imagen(self.enemy_1_sprite_run_img, pygame.Rect((x,0) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_1_run_imgs.append(subimage)
            self.enemy_1_run2_imgs.append(pygame.transform.flip(subimage,True,False))
        
        for x in range(0, self.enemy_1_sprite_hit_img.get_width(), 106):
            subimage, rect = divide_imagen(self.enemy_1_sprite_hit_img, pygame.Rect((x,0) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_1_hit_imgs.append(subimage)
            self.enemy_1_hit2_imgs.append(pygame.transform.flip(subimage,True,False))


        


    def draw(self, window, camera):
        extra_offset = 0
        direction = self.path[self.segment]["dir"]
        if self.current_animation == "run":
            self.sprite_count += 1
            if direction == (-1,0):
                if self.sprite_count >= len(self.enemy_1_run2_imgs) * 6:
                    self.sprite_count = 0
                current_sprite = pygame.transform.scale(self.enemy_1_run2_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
                extra_offset = -128 

            else:
                if self.sprite_count >= len(self.enemy_1_run_imgs) * 6:
                    self.sprite_count = 0
                current_sprite = pygame.transform.scale(self.enemy_1_run_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))

    
        elif self.current_animation == "hit":
            self.sprite_count += 1

            if direction == (-1,0):
                if self.sprite_count >= len(self.enemy_1_hit2_imgs) * 6:
                    self.sprite_count = 0
                    self.current_animation = "run"
                current_sprite = pygame.transform.scale(self.enemy_1_hit2_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))
                extra_offset = -128 

            else:
                if self.sprite_count >= len(self.enemy_1_hit_imgs) * 6:
                    self.sprite_count = 0
                    self.current_animation = "run"
                current_sprite = pygame.transform.scale(self.enemy_1_hit_imgs[self.sprite_count // 6], (self.tam_sprite[0]*2, self.tam_sprite[1]*2))


        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0] + extra_offset), (self.Y + camera.Y + self.offset_sprite[1])) )
        self.draw_health_bar(window, camera)
        



class EnemyTank(Enemy):

    def __init__(self,path,grid):
        self.vel = 0.5
        self.max_health = 100
        self.health = 100
        self.chatarra = 8
        self.subject = EnemySubject()
        self.killed = False

        self.path = path
        self.segment = 0 # indice do segmento do percorrido
        world_pos = grid.map_to_world((path[0]["ini"][0], path[0]["ini"][1])) 
        self.X = world_pos[0]
        self.Y = world_pos[1]

        # Cousas dos sprites
        self.current_animation = "run"
        self.offset_sprite = (-48, -48)
        self.sprite_count = 0

        self.name = 'tanque'

        self.enemy_2_run_imgs = []
        self.enemy_2_hit_imgs = []
        self.enemy_2_sprite_run_img = pygame.image.load(os.path.join("Assets/sprites/enemy_tank", "enemy_2_run.png")).convert_alpha()
        self.enemy_2_sprite_hit_img = pygame.image.load(os.path.join("Assets/sprites/enemy_tank", "enemy_2_hit.png")).convert_alpha()
        self.tam_sprite = (96,96)
        for x in range(0, self.enemy_2_sprite_run_img.get_width(), 96):
            subimage, rect = divide_imagen(self.enemy_2_sprite_run_img, pygame.Rect((x,0) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_2_run_imgs.append(subimage)
        
        for x in range(0, self.enemy_2_sprite_hit_img.get_width(), 96):
            subimage, rect = divide_imagen(self.enemy_2_sprite_hit_img, pygame.Rect((x,0) ,(self.tam_sprite[0],self.tam_sprite[1]) ))
            self.enemy_2_hit_imgs.append(subimage)

        

    def draw(self, window, camera):
        extra_offset = 0
        if self.current_animation == "run":
            self.sprite_count += 1
            if self.sprite_count >= len(self.enemy_2_run_imgs) * 6:
                self.sprite_count = 0
            current_sprite = self.enemy_2_run_imgs[self.sprite_count // 6]

    
        elif self.current_animation == "hit":
            self.sprite_count += 1
            if self.sprite_count >= len(self.enemy_2_hit_imgs) * 6:
                self.sprite_count = 0
                self.current_animation = "run"
            current_sprite = self.enemy_2_hit_imgs[self.sprite_count // 6]

        window.blit(current_sprite, ((self.X + camera.X + self.offset_sprite[0] + extra_offset), (self.Y + camera.Y + self.offset_sprite[1])) )
        self.draw_health_bar(window, camera)
