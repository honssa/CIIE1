import pygame
import os
from escena import Escena
from menu.pause_menu import PauseMenu

ANCHO=1340
ALTO=700

class Director():
	def __init__(self):
		self.win = pygame.display.set_mode((ANCHO, ALTO))
		pygame.display.set_caption("O último bastión")
		self.pila=[]
		self.salir_escena=False
		self.clock=pygame.time.Clock()
		pygame.mouse.set_visible(False)	# Facemos que o cursor sexa invisible e o reemplazamos por unha imaxe
		self.pointerImg = pygame.image.load(os.path.join("Assets/cursors", "basic.png")).convert_alpha()
		self.pointerImg_rect = self.pointerImg.get_rect()
		self.trigger_secreta = False # Dispara a escena secreta cando e true


	def bucle(self, escena):
		self.salir_escena=False
		pygame.event.clear()

		while not self.salir_escena:
			tiempo_pasado=self.clock.tick(60)
			escena.eventos(pygame.event.get())
			escena.update(tiempo_pasado)
			# Actualizar posicion do cursor
			self.pointerImg_rect.center = pygame.mouse.get_pos()
			escena.dibujar(self.win)
			# Debuxar o cursor
			self.win.blit(self.pointerImg, self.pointerImg_rect)
			pygame.display.flip()

	def ejecutar(self):
		while (len(self.pila)>0):
			self.bucle(self.pila[len(self.pila)-1])

	def salirEscena(self):
		self.salir_escena=True
		if(len(self.pila)>0):
			self.pila.pop()

	def salirPrograma(self):
		self.pila=[]
		self.salir_escena=True

	def apilarEscena(self, escena): #la misma escena puede volver
		self.salir_escena=True
		self.pila.append(escena)

	def cambiarEscena(self, escena): #la escena no vuelve
		self.salirEscena()
		self.pila.append(escena)
	
	def pauseGame(self):
		self.apilarEscena(PauseMenu(self))
	
	def set_cursor_image(self, img):
		self.pointerImg = img
		self.pointerImg_rect = self.pointerImg.get_rect()
