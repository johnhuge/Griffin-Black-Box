#! /usr/bin/env python3

if __name__ == 'gui':
	import sys
	import pygame
	import pygame.gfxdraw	#WARNING gfxdraw is experimantal and future versions of pygame may not support it, be careful
	import math


class Gui():
	
	black = 0, 0, 0
	white = 255, 255, 255
	red = 255, 0, 0
	green = 0, 255, 0
	blue = 0, 0, 255
	unipgRed = 237, 28, 36


	def __init__(self, GuiPipeGuiEnd):

		self.GuiPipeGuiEnd = GuiPipeGuiEnd

		self.config()

		self.screen = pygame.display.set_mode(self.size)

		self.clock = pygame.time.Clock()

		pygame.font.init()
		self.myfont30 = pygame.font.Font(pygame.font.match_font('segoeuisemibold'), 30)
		self.myfont120 = pygame.font.Font(pygame.font.match_font('segoeuisemibold'), 120)

		self.background = pygame.image.load('SfondoMiniCockpit.png').convert()
		self.backrect = self.background.get_rect()

		self.foreground = pygame.image.load('MiniCockpit.png').convert_alpha()
		self.forerect = self.foreground.get_rect()


	def config(self):
		import configparser

		config = configparser.ConfigParser()
		config.read('settings.cfg')

		self.size = self.width, self.height = config.getint('video settings', 'width'), config.getint('video settings', 'height')

		self.variables = {}
		for i in config['variables']:
			if (config.getboolean('variables', i)):
				self.variables[i]=-1

		self.leftRectVar = config.get('rects', 'left')
		self.rightRectVar = config.get('rects', 'right')

		self.max = {}
		for i in config['absolute max']:
			self.max[i] = config.getfloat('absolute max', i)


	def updateGraphics(self):

		self.updateVariables()
		self.screen.blit(self.background, self.backrect)
		self.updateRects()
		self.updateRPMdial(self.screen)
		self.screen.blit(self.foreground, self.forerect)
		self.updateTexts()
		self.updateIcons()


	def updateRPMdial(self, surface, color=white, radius=200):

		nsectors = int(self.max['rpm']/209 if self.max['rpm']%1 == 0.0 else (self.max['rpm']/9)+1)
		centerx = int(self.width/2)
		centery = int(self.height/2)
		theta0 = math.radians(29)
		theta1 = math.radians((211-(182*self.variables['rpm']/self.max['rpm'])))
		dtheta = (theta1 - theta0) / nsectors
		sectors = [theta0 + n*dtheta for n in range(nsectors + 1)] 

		points = [(centerx, centery)] + [(centerx + radius * math.cos(theta), centery - radius * math.sin(theta)) for theta in sectors]

		pygame.gfxdraw.filled_polygon(surface, points, color)


	def updateVariables(self):

		 while self.GuiPipeGuiEnd.poll(0.001):
		 	self.variables = self.GuiPipeGuiEnd.recv()


	def updateTexts(self):

		self.rpmtextSurface = self.myfont30.render(str(self.variables["rpm"]), True, Gui.white)
		self.rpmtextRect = self.rpmtextSurface.get_rect()
		self.screen.blit(
		self.rpmtextSurface, 
		pygame.Rect(
			int((self.width-self.rpmtextRect.width)/2), 
			int((self.height-self.rpmtextRect.height)/2)+60, 
			int((self.width+self.rpmtextRect.width)/2), 
			int((self.height+self.rpmtextRect.height)/2)+60
			)
		)

		self.speedtextSurface = self.myfont120.render(str(int(self.variables["t_h20"]*3/440)), True, Gui.white)
		self.speedtextRect = self.speedtextSurface.get_rect()
		self.speedtextSurface, 
		self.screen.blit(
			self.speedtextSurface,
			pygame.Rect(
				int((self.width-self.speedtextRect.width)/2), 
				int((self.height-self.speedtextRect.height)/2)-30, 
				int((self.width+self.speedtextRect.width)/2), 
				int((self.height+self.speedtextRect.height)/2)-30
			)
		)


	def updateRects(self):
		#TODO
		pass


	def updateIcons(self):
		#TODO
		pass


	def loop(self):

		while True:

			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit(0)

			pygame.event.pump()

			self.updateVariables()

			self.updateGraphics()

			self.clock.tick(60)

			self.fpstextSurface = self.myfont30.render(str(int(self.clock.get_fps())), True, Gui.green)
			self.screen.blit(self.fpstextSurface, self.fpstextSurface.get_rect())

			pygame.display.flip()


"""
TODO:
conta marce
labels per le altre variabili
icone per le spie
rettangoli per barre laterali
tk per le impostazioni
media velocità ruote
touch per impostazioni
tasto per dump to usb drive

"""

if __name__ == '__main__':
	import os

	bashCommand = "/usr/bin/env python3 ./launcher.py"
	os.system(bashCommand)
