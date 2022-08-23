import pygame
from escena import Escena
import os
from dialogs.dialog_scene import Dialogos

class Seleccion(Escena):
	def __init__(self, director, nivel):
		Escena.__init__(self, director)
		w=director.win.get_width()
		h=director.win.get_height()
		self.fondo= pygame.transform.scale(pygame.image.load(os.path.join("Assets","seleccion de personaje.png")),(w, h)).convert_alpha()
		self.hover_seleccion = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","hover_seleccion.png")),(w, h)).convert_alpha()
		self.hover = 0 # 0: nada // 1: Rock // 2: Paper // 3: Scissors
		self.nivel = nivel

		# PORTRAITS
		self.portrait_chema = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","chema.png")),(186, 186)).convert_alpha()
		self.portrait_olen = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","olen.png")),(186, 186)).convert_alpha()
		self.portrait_rock = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","rock.png")),(210, 210)).convert_alpha()
		self.portrait_paper = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","paper.png")),(210, 210)).convert_alpha()
		self.portrait_scissors = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","scissors.png")),(186, 186)).convert_alpha()
		self.portrait_ludwig = pygame.transform.scale(pygame.image.load(os.path.join("Assets/dialogos","ludwig.png")),(186, 186)).convert_alpha()

		# Dialogos
		self.dialogos_nivel_1 = []
		self.dialogo1 = []
		self.dialogo1.append("Parece que entraron polo noroeste, debemos bloquear o seu paso para que non cheguen a entrada.")
		self.dialogo1.append("As torres que podes usar están no panel dereito da interfaz de control, as torres verdes son boas disparando rápido;")
		self.dialogo1.append("As azuis disparan proxectiles de artilleria que causan unha explosión ao impactar, e as vermellas fan dano acumulativo,")
		self.dialogo1.append("moi util contra enemigos lentos.")
		self.dialogo1.append("Recorda que te podes desprazar polo mapa pulsando w, a, s, d")
		self.dialogo1.append("En fin, boa sorte na batalla compañeiro.")

		self.dialogo1_rock = []	# Pequenas variacions entre comandantes
		self.dialogo1_rock.append((self.dialogo1[0], 1))
		self.dialogo1_rock.append(("Teño as tropas preparadas, eses trozos de ferralla non pasaran mentres quede un de nos con vida.", 1))
		self.dialogo1_rock.append((self.dialogo1[1], 1))
		self.dialogo1_rock.append((self.dialogo1[2], 1))
		self.dialogo1_rock.append((self.dialogo1[3], 1))
		self.dialogo1_rock.append((self.dialogo1[4], 1))
		self.dialogo1_rock.append((self.dialogo1[5], 1))

		self.dialogo1_paper = []	# Pequenas variacions entre comandantes
		self.dialogo1_paper.append((self.dialogo1[0], 2))
		self.dialogo1_paper.append(("...", 2))
		self.dialogo1_paper.append(("Non son moito de falar como podes ver.", 2))
		self.dialogo1_paper.append((self.dialogo1[1], 2))
		self.dialogo1_paper.append((self.dialogo1[2], 2))
		self.dialogo1_paper.append((self.dialogo1[3], 2))
		self.dialogo1_paper.append((self.dialogo1[4], 2))
		self.dialogo1_paper.append((self.dialogo1[5], 2))

		self.dialogo1_scissors = []	# Pequenas variacions entre comandantes
		self.dialogo1_scissors.append((self.dialogo1[0], 3))
		self.dialogo1_scissors.append(("Teño as tropas motivadas, esto vai ser unha tralla de moito coidado.", 3))
		self.dialogo1_scissors.append(("Canto tempo facía que non tiña algo de acción hahaha.", 3))
		self.dialogo1_scissors.append((self.dialogo1[1], 3))
		self.dialogo1_scissors.append((self.dialogo1[2], 3))
		self.dialogo1_scissors.append((self.dialogo1[3], 3))
		self.dialogo1_scissors.append((self.dialogo1[4], 3))
		self.dialogo1_scissors.append((self.dialogo1[5], 3))



		self.dialogos_nivel_2 = []
		self.dialogo2 = []
		self.dialogo2.append("Estamos sendo atacados por dous flancos, o NORTE e o ESTE. Hai que impedir que inflinxan un dano critico as nosas defensas.")
		self.dialogo2.append("Lembra que podes mellorar as torres usando as baterías, un item que as veces se atopa nos enxeñeiros inimigos.")
		self.dialogo2.append("As torres melloradas son bastante máis efectivas pero pensa que non vas poder obter de volta as baterías invertidas se as reciclas.")
		self.dialogo2.append("Decide ben en que torre queres gastalas.")
		self.dialogo2.append("En fin, boa sorte na batalla compañeiro.")


		self.dialogo2_rock = []	# Pequenas variacions entre comandantes
		self.dialogo2_rock.append(("Parece que as lesmas metálicas teñen ganas de outra malleira.", 1))
		self.dialogo2_rock.append(("Nunca entrarán no fort Knox, non mentres ROCK quede con vida e con balas de sobra.", 1))
		self.dialogo2_rock.append((self.dialogo2[0], 1))
		self.dialogo2_rock.append((self.dialogo2[1], 1))
		self.dialogo2_rock.append((self.dialogo2[2], 1))
		self.dialogo2_rock.append((self.dialogo2[3], 1))
		self.dialogo2_rock.append((self.dialogo2[4], 1))


		self.dialogo2_paper = []	# Pequenas variacions entre comandantes
		self.dialogo2_paper.append(("...", 2))
		self.dialogo2_paper.append(("Tanto ten o resultado desta batalla... ", 2))
		self.dialogo2_paper.append(("Os nosos esforzos son inutiles.", 2))
		self.dialogo2_paper.append((self.dialogo2[0], 2))
		self.dialogo2_paper.append((self.dialogo2[1], 2))
		self.dialogo2_paper.append((self.dialogo2[2], 2))
		self.dialogo2_paper.append((self.dialogo2[3], 2))
		self.dialogo2_paper.append((self.dialogo2[4], 2))


		self.dialogo2_scissors = []	# Pequenas variacions entre comandantes
		self.dialogo2_scissors.append(("Vamoooooooooos chavalada.", 3))
		self.dialogo2_scissors.append(("Toca repartir lume, hostia.", 3))
		self.dialogo2_scissors.append((self.dialogo2[0], 3))
		self.dialogo2_scissors.append((self.dialogo2[1], 3))
		self.dialogo2_scissors.append((self.dialogo2[2], 3))
		self.dialogo2_scissors.append((self.dialogo2[3], 3))
		self.dialogo2_scissors.append((self.dialogo2[4], 3))



		self.dialogos_nivel_3 = []
		self.dialogo3 = []
		self.dialogo3.append("Estamos sendo rodeados por catro flancos Norte, Sur, Este e Oeste.")
		self.dialogo3.append("Desta batalla depende a nosa supervivencia.")
		self.dialogo3.append("Aproveita os lugares onde unha torre poida disparar a máis dun camiño.")
		self.dialogo3.append("En fin, boa sorte na batalla compañeiro.")

		self.dialogo3_rock = []	# Pequenas variacions entre comandantes
		self.dialogo3_rock.append(("Temos que paralos, e o noso deber.", 1))
		self.dialogo3_rock.append(("Estos momentos de incertidume son sempre os mais difíciles.", 1))
		self.dialogo3_rock.append(("Capaz sexa débil e fácil de enganar pero o meu honor e o meu corazón e forte.", 1))
		self.dialogo3_rock.append((self.dialogo3[0], 1))
		self.dialogo3_rock.append((self.dialogo3[1], 1))
		self.dialogo3_rock.append((self.dialogo3[2], 1))
		self.dialogo3_rock.append((self.dialogo3[3], 1))

		
		self.dialogo3_scissors = []
		self.dialogo3_scissors.append(("Pinta dificil, eh?",3))
		self.dialogo3_scissors.append(("Hahaha non te preocupes vai ser todo un festín de pólvora, confía en min.",3))
		self.dialogo3_scissors.append((self.dialogo3[0], 3))
		self.dialogo3_scissors.append((self.dialogo3[1], 3))
		self.dialogo3_scissors.append((self.dialogo3[2], 3))
		self.dialogo3_scissors.append((self.dialogo3[3], 3))



		self.dialogos_nivel_1.append(self.dialogo1_rock)
		self.dialogos_nivel_1.append(self.dialogo1_paper)
		self.dialogos_nivel_1.append(self.dialogo1_scissors)

		self.dialogos_nivel_2.append(self.dialogo2_rock)
		self.dialogos_nivel_2.append(self.dialogo2_paper)
		self.dialogos_nivel_2.append(self.dialogo2_scissors)

		self.dialogos_nivel_3.append(self.dialogo3_rock)
		self.dialogos_nivel_3.append([])
		self.dialogos_nivel_3.append(self.dialogo3_scissors)


	def update(self, tiempo):
		x, y = pygame.mouse.get_pos()
		if (45 <= x <= 45+1255) and (15 <= y <= 15+205): #rock
			self.hover = 1
		elif (45 <= x <= 45+1255) and (245 <= y <= 245+205): #paper
			self.hover = 2
		elif (45 <= x <= 45+1255) and (475 <= y <= 475+205): #scissors
			self.hover = 3
		else:
			self.hover = 0


	
	def eventos(self, lista_eventos):
		for event in lista_eventos:
			if event.type == pygame.QUIT:
				self.director.salirPrograma()

			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				x, y = pygame.mouse.get_pos()
				if self.nivel == 1:
					dialogo = self.dialogos_nivel_1
				elif self.nivel == 2:
					dialogo = self.dialogos_nivel_2
				elif self.nivel == 3:
					dialogo = self.dialogos_nivel_3

				if self.hover == 1:
					escena = Dialogos(self.director, "rock", dialogo[0], "c", self.nivel)
					self.director.cambiarEscena(escena)
				elif self.hover == 2:
					if self.nivel != 3:	# No ultimo nivel paper non esta
						escena = Dialogos(self.director, "paper", dialogo[1],"c",self.nivel)
						self.director.cambiarEscena(escena)
				elif self.hover == 3:
					escena = Dialogos(self.director, "scissors", dialogo[2],"c",self.nivel)
					self.director.cambiarEscena(escena)
	
	def dibujar(self, win):
		win.blit(self.fondo, (0,0))

		if self.hover == 1:
			win.blit(self.hover_seleccion, (0,0))
		elif self.hover == 2:
			if self.nivel != 3:
				win.blit(self.hover_seleccion, (0,230))
		elif self.hover == 3:
			win.blit(self.hover_seleccion, (0,460))
		
		win.blit(self.portrait_rock, (85,-8))
		win.blit(self.portrait_paper, (87,216))
		win.blit(self.portrait_scissors, (95,470))
		