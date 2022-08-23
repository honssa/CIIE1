import pygame
from escena import Escena
from levels.level import Level1, Level2, Level3
import os



def divide_imagen(image, rect):
    subimage = image.subsurface(rect)
    return subimage, rect


def draw_text_2(text, font, COLOUR, POS, window):
    text_surf = font.render(text, True, COLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = (POS[0] + text_rect.width//2, POS[1]) 
    window.blit(text_surf, text_rect)


class Dialogos(Escena):
	def __init__(self, director, comander, dialogos, personaxe, sig):
		Escena.__init__(self, director)
		w=director.win.get_width()
		h=director.win.get_height()
		self.finDialogo=False
		self.chema= pygame.transform.scale(pygame.image.load(os.path.join("Assets","pantalla dialogos chema 2.png")),(w, h)).convert_alpha()
		self.olen= pygame.transform.scale(pygame.image.load(os.path.join("Assets","pantalla dialogos olen.png")),(w, h)).convert_alpha()

		# Cadro de dialogo
		self.cadro_dialogo = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","cadro_dialogo.png")),(w, h)).convert_alpha()
		self.cadro_dialogo2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","cadro_dialogo_2.png")),(w, h)).convert_alpha()

		# PORTRAITS
		self.portrait_chema = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","chema.png")),(272, 272)).convert_alpha()
		self.portrait_olen = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","olen.png")),(272, 272)).convert_alpha()
		self.portrait_rock = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","rock.png")),(272, 272)).convert_alpha()
		self.portrait_paper = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","paper.png")),(272, 272)).convert_alpha()
		self.portrait_scissors = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","scissors.png")),(272, 272)).convert_alpha()
		self.portrait_ludwig = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","ludwig.png")),(272, 272)).convert_alpha()

		# Cousas de falar
		self.chema_falar = pygame.image.load(os.path.join("Assets/dialogos","chema_falar.png")).convert_alpha()
		self.olen_falar = pygame.image.load(os.path.join("Assets/dialogos","olen_falar.png")).convert_alpha()
		self.rock_falar = pygame.image.load(os.path.join("Assets/dialogos","rock_falar.png")).convert_alpha()
		self.paper_falar = pygame.image.load(os.path.join("Assets/dialogos","paper_falar.png")).convert_alpha()
		self.scissors_falar = pygame.image.load(os.path.join("Assets/dialogos","scissors_falar.png")).convert_alpha()

		# Cousas dos fondos (Nos dialogos post-seleccion)
		self.fondo_nvl1 = pygame.image.load(os.path.join("Assets/dialogos","fondo_dialogo_nv1.png")).convert_alpha()
		self.fondo_nvl23 = pygame.image.load(os.path.join("Assets/dialogos","fondo_dialogo_nv23.png")).convert_alpha()

		# Cousas do parallax (que agora realmente so e unha animacion)
		self.tam_bg = (544, 320) 		 # 272,160
		self.tam_layer1 = (426, 284)	 # 213,142
		self.tam_layer2 = (544, 300)	 # 272,150
		self.tam_layer3 = (544, 208)	 # 272,104
		self.p_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos/parallax-industrial-pack","bg.png")).convert_alpha(), self.tam_bg)
		self.p_layer1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos/parallax-industrial-pack","layer1.png")).convert_alpha(), self.tam_layer1)
		self.p_layer2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos/parallax-industrial-pack","layer2.png")).convert_alpha(), self.tam_layer2)
		self.p_layer3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos/parallax-industrial-pack","layer3.png")).convert_alpha(), self.tam_layer3)

		self.tiras_layer1 = []
		self.tiras_layer2 = []
		self.tiras_layer3 = []

		pygame.mixer.stop()
		self.pos_bg = (380,50)
		self.pos_layer1 = (self.pos_bg[0], self.pos_bg[1]+36)
		self.pos_layer2 = (self.pos_bg[0], self.pos_bg[1]+20)
		self.pos_layer3 = (self.pos_bg[0], self.pos_bg[1]+112)

		self.despl = 0 	# Move o layer 1
		self.despl2 = 0 # Move o layer 2
		self.despl3 = 0 # Move o layer 3
		self.counter_draw = 0

		for x in range(0, self.p_layer1.get_width()):
			subimage, rect = divide_imagen(self.p_layer1, pygame.Rect((x,0) ,(1,self.tam_layer1[1]) ))
			self.tiras_layer1.append(subimage)
		for x in range(0, self.p_layer2.get_width()):
			subimage, rect = divide_imagen(self.p_layer2, pygame.Rect((x,0) ,(1,self.tam_layer2[1]) ))
			self.tiras_layer2.append(subimage)
		for x in range(0, self.p_layer3.get_width()):
			subimage, rect = divide_imagen(self.p_layer3, pygame.Rect((x,0) ,(1,self.tam_layer3[1]) ))
			self.tiras_layer3.append(subimage)

		pygame.mixer.Sound("Sounds/industrial.ogg").play(-1)

		self.dialogos = []
		self.quen_fala = [] #personaxe  # 0: Chema // 1: Rock // 2: Paper // 3 Scissors // 4: Olen // 5: ???
		for dialogo in dialogos:
			self.dialogos.append(dialogo[0])
			self.quen_fala.append(dialogo[1])
		self.MAX_DIALOG=len(self.dialogos)
		self.num=0 
		self.aux=""
		self.i=0
		self.comander = comander
		self.sig=sig #siguiente nivel del juego que se tiene que cargar despues de esta escena

	def update(self, *args):
		pass
	
	def eventos(self, lista_eventos):
		for event in lista_eventos:
			if event.type == pygame.QUIT:
				self.director.salirPrograma()
			if self.num>=self.MAX_DIALOG-1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pygame.mixer.stop()
				if self.sig==1:
					escena = Level1(self.director, self.comander)
				elif self.sig==2: # Esto vai de 2 dialogo (pre-seleccion) a seleccion (nivel 2)
					escena = Level2(self.director, self.comander)
				elif self.sig == 3:
					escena = Level3(self.director, self.comander)
				elif self.sig == 4:
					from dialogs.cinematica_final import Cinematica
					escena = Cinematica(self.director)
				elif self.sig == 8:	# Esto vai de intro a 1 dialogo (pre-seleccion)
					escena = Dialogos(self.director, self.comander, dialogo, "o", 9)
				elif self.sig == 9: # Esto vai de 1 dialogo (pre-seleccion) a seleccion (nivel 1)
					from selection import Seleccion
					escena = Seleccion(self.director, 1)
				elif self.sig == 10: # Esto vai de 2 dialogo (pre-seleccion) a seleccion (nivel 2)
					from selection import Seleccion
					escena = Seleccion(self.director, 2)
				elif self.sig == 11: # Esto vai de 3 dialogo (pre-seleccion) a seleccion (nivel 3)
					from selection import Seleccion
					escena = Seleccion(self.director, 3)
				self.director.cambiarEscena(escena)
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.finDialogo==True:
				self.num+=1
				self.i=0
				self.aux=""
				self.finDialogo=False

	def dibujar(self, win):
		letra_px = 'Assets/fonts/Avenixel-Regular.ttf'
		fuente = pygame.font.Font(letra_px, int(27))
		fonte_grande = pygame.font.Font(letra_px, int(54))
		win.fill((0,0,0))
		win.blit(self.p_bg, self.pos_bg)

		if self.sig == 1 or self.sig == 2 or self.sig == 3:
			# Pintamos o fondo
			if self.sig == 1:
				win.blit(self.fondo_nvl1, (0,0))
			elif self.sig == 2 or self.sig == 3:
				win.blit(self.fondo_nvl23, (0,0))

		else: 
			# pintar as tiras
			if self.counter_draw == 3:
				self.despl += 1
				self.despl2 += 2
				self.despl3 += 4
				self.counter_draw = 0
			else:
				self.counter_draw += 1
			#depl_local = self.despl % 272
			for i1 in range(len(self.tiras_layer1)):
				win.blit(self.tiras_layer1[i1], (self.pos_layer1[0] + ((i1 + self.despl) % 544), self.pos_layer1[1]))
			for i2 in range(len(self.tiras_layer2)):
				win.blit(self.tiras_layer2[i2], (self.pos_layer2[0] + ((i2 + self.despl2) % 544), self.pos_layer2[1]))
			for i3 in range(len(self.tiras_layer3)):
				win.blit(self.tiras_layer3[i3], (self.pos_layer3[0] + ((i3 + self.despl3) % 544), self.pos_layer3[1]))

		if self.num >= len(self.quen_fala):
			pass
		elif self.quen_fala[self.num] == 0: # Fala chema
			win.blit(self.cadro_dialogo, (0,0))
			win.blit(self.portrait_chema, (50,378))
			draw_text_2("CHEMA JENKINS", fonte_grande, (255,255,255), (330,480), win)
		elif self.quen_fala[self.num] == 1: # Fala rock
			win.blit(self.cadro_dialogo, (0,0))
			win.blit(self.portrait_rock, (50,378))
			draw_text_2("ROCK", fonte_grande, (255,255,255), (330,480), win)
		elif self.quen_fala[self.num] == 2: # Fala paper
			win.blit(self.cadro_dialogo, (0,0))
			win.blit(self.portrait_paper, (50,378))
			draw_text_2("PAPER", fonte_grande, (255,255,255), (330,480), win)
		elif self.quen_fala[self.num] == 3: # Fala scissors
			win.blit(self.cadro_dialogo, (0,0))
			win.blit(self.portrait_scissors, (50,378))
			draw_text_2("SCISSORS", fonte_grande, (255,255,255), (330,480), win)
		elif self.quen_fala[self.num] == 4: # Fala olen
			win.blit(self.cadro_dialogo2, (0,0))
			win.blit(self.portrait_olen, (50,378))
			draw_text_2("OLEN SKUM", fonte_grande, (255,255,255), (330,480), win)

		if not (self.num>=self.MAX_DIALOG-1):
			textoEntradaSize=len(self.dialogos[self.num])	
		else:
			self.num = self.MAX_DIALOG-1
			textoEntradaSize=len(self.dialogos[self.num])

		if self.i<textoEntradaSize:
			self.aux+=self.dialogos[self.num][self.i]
			self.i+=1
		else:
			self.finDialogo=True

		self.blit_text(win, (330, 505), fuente)


	def blit_text(self, surface, pos, font, color=pygame.Color('white')):
		words = [word.split(' ') for word in self.aux.splitlines()]  
		space = font.size(' ')[0]  
		max_width = surface.get_width()-75
		max_height = surface.get_height()-75
		x, y = pos
		for line in words:
			for word in line:
				word_surface = font.render(word, 0, color)
				word_width, word_height = word_surface.get_size()
				if x + word_width >= max_width:
					x = pos[0]  
					y += word_height  
				surface.blit(word_surface, (x, y))
				x += word_width + space
			x = pos[0]  
			y += word_height  


			
