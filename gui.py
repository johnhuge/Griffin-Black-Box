#! /usr/bin/env python3

if __name__ == 'gui':
	import sys
	import pygame
	import pygame.gfxdraw	#WARNING gfxdraw is experimantal and future versions of pygame may not support it, be careful
	import math
	import ast

	sys.stdout.flush()

def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

class Gui:
	
	black = 0, 0, 0
	white = 255, 255, 255
	red = 255, 0, 0
	green = 0, 255, 0
	blue = 0, 0, 255
	unipgRed = 237, 28, 36
	bestemmie=[1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1]

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

		self.settingsIcon = pygame.image.load('settings.png').convert_alpha()
		self.settingsIconRect = self.settingsIcon.get_rect().move(0,-1)
		self.settingsIconVisible = True
		self.settingsIconCount = 0

		self.leftRect = pygame.Rect(58, 46, 145, 388)
		self.leftRectStuffing = pygame.Surface((self.leftRect.width, self.height))

		# self.count = 0

		self.rightRect = pygame.Rect(597, 46, 145, 388)
		self.rightRectStuffing = pygame.Surface((self.leftRect.width, self.height))
		

	def animateSettingsIcon(self):
		# print(self.settingsIconRect.collidepoint((39,39)))
#		if self.settingsIconVisible and self.settingsIconRect.collidepoint((39,39)): #è visibile e deve esserlo
#			print('vis e dovrebbe')
#			sys.stdout.flush()
#			return

		elif self.settingsIconVisible and not self.settingsIconRect.collidepoint((39,39)): #non è visibile ma dovrebbe esserlo
#			print('non vis ma dovrebbe')
#			sys.stdout.flush()
			self.settingsIconRect = self.settingsIconRect.move((0, Gui.bestemmie[self.settingsIconCount]))

			if self.settingsIconCount>0:
				self.settingsIconCount -= 1

		elif not self.settingsIconVisible and self.settingsIconRect.collidepoint((1,0)): #è visibile ma non dovrebbe esserlo
			self.settingsIconRect = self.settingsIconRect.move((0,-Gui.bestemmie[self.settingsIconCount]))

			# if self.settingsIconCount< 27:
			if self.settingsIconCount< 21:
				self.settingsIconCount += 1

		else: # non è visibile e non dovrebbe esserlo
			return





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

		# while exists := False:
		# 	for i in config['absolute max']:
		# 		if i == self.variables[self.leftRectVar]:
		# 			exists = False
		# 			self.leftRectVarHasMax = True
		# 	self.max[self.variables[self.leftRectVar]] = 0
		# 	self.leftRectVarHasMax = False


		self.widgetsPositions = {}
		for i in config['widgets position']:
			self.widgetsPositions[i] = ast.literal_eval(config.get("widgets position", i))


	def updateGraphics(self):

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

		# if self.variables['rpm'] > 4000:		#modificami								#AAAAAAAAAAAAAAAAAAH
		# 	self.settingsIconVisible = False
		# else:
		# 	self.settingsIconVisible = True


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
		# self.speedtextSurface, 
		self.screen.blit(
			self.speedtextSurface,
			pygame.Rect(
				int((self.width-self.speedtextRect.width)/2), 
				int((self.height-self.speedtextRect.height)/2)-30, 
				int((self.width+self.speedtextRect.width)/2), 
				int((self.height+self.speedtextRect.height)/2)-30
			)
		)

		self.variablesLabels = {}
		print(self.variablesLabels)
		for i in self.variables:
			if i != "rpm" and i !="vel_fsx" and i !="vel_fdx" and i !="vel_rsx" and i !="vel_rdx":
				self.variablesLabels[i] = self.myfont30.render(str(i) + " = " + str(self.variables[i]), True, Gui.black)
				self.screen.blit(
					self.variablesLabels[i], 
					pygame.Rect(
						self.widgetsPositions[i]['x'], 
						self.widgetsPositions[i]['y'],
						self.variablesLabels[i].get_rect().width,
						self.variablesLabels[i].get_rect().height,
						)
					)





	def updateRects(self):
		#TODO
		if self.variables[self.leftRectVar]:
			pass
		self.leftRect = pygame.Rect(58, abs(388+46-(388*self.variables[self.leftRectVar]/self.max[self.leftRectVar])), 145, abs((388*self.variables[self.leftRectVar]/self.max[self.leftRectVar])-388-46))
		self.rightRect = pygame.Rect(597, abs(388+46-(388*self.variables[self.rightRectVar]/self.max[self.rightRectVar])), 145, abs((388*self.variables[self.rightRectVar]/self.max[self.rightRectVar])-388-46))

		self.leftRectStuffing.fill(Gui.green)
		self.rightRectStuffing.fill(Gui.green)

		self.screen.blit(self.rightRectStuffing, self.rightRect)
		self.screen.blit(self.leftRectStuffing, self.leftRect)
		# pass


	def updateIcons(self):
		self.animateSettingsIcon()
		self.screen.blit(self.settingsIcon, self.settingsIconRect)

		# self.settingsIcon = pygame.Rect(0,0,40,40)
		# pygame.draw.rect(self.screen, [25, 0, 0], self.settingsIcon)
		# self.screen.blit(self.settingsIcon)

		#TODO
		# pass


	def loop(self):

		while True:

			for event in pygame.event.get():
				# if event.type == pygame.QUIT: sys.exit(0)
				if event.type == pygame.QUIT: sys.exit('gui left the chat')
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.settingsIconRect.collidepoint(event.pos):
						raise Exception('accessing settings')
					else:															#eliminare nella release ufficiale
						self.settingsIconVisible = not self.settingsIconVisible
						print(self.settingsIconVisible)
						sys.stdout.flush()
				# if event.type == pygame.QUIT: raise Exception('accessing settings')
				# if event.type == pygame.QUIT: 
				# 	import signal 
				# 	signal.raise_signal(signal.SIGKILL)

			pygame.event.pump()

			# self.count +=1

			self.updateVariables()

			self.updateGraphics()

			self.clock.tick(60)

			self.fpstextSurface = self.myfont30.render(str(int(self.clock.get_fps())), True, Gui.green)
			# self.screen.blit(self.fpstextSurface, self.fpstextSurface.get_rect())

			pygame.display.flip()


"""
TODO:
conta marce
labels per le altre variabili
icone per le spie
rettangoli per barre laterali -----DONE ???
tk per le impostazioni ------------DONE	
media velocità ruote
touch per impostazioni ------------DONE
tasto per dump to usb drive


BUGs:
se una variabile non ha la spunta ma è selezionata su uno dei rettangoli, crasha tutto
"""

if __name__ == '__main__':
	import os

	bashCommand = "/usr/bin/env python3 ./launcher.py"
	os.system(bashCommand)
