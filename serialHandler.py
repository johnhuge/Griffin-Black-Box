#! /usr/bin/env python3

if __name__ == 'serialHandler':
	import serial
	import time
	import codecs
	import ast


class SerialHandler:


	def __init__(self, GuiPipeSerialEnd, FHPipeSerialEnd):

		self.GuiPipeSerialEnd = GuiPipeSerialEnd
		self.FHPipeSerialEnd = FHPipeSerialEnd

		self.lastGuiUpdate = time.time()

		self.config()

		if 'endchar' in self.settings and type(self.settings['endchar']) == type('a string'):
			self.settings['endchar'] = bytes(codecs.decode(self.settings['endchar'], 'unicode_escape'), encoding = 'utf8')

		if 'startchar' in self.settings and type(self.settings['startchar']) == type('a string'):
			self.settings['startchar'] = bytes(codecs.decode(self.settings['startchar'], 'unicode_escape'), encoding = 'utf8')


		self.serialInstance = serial.Serial(port = self.settings['name'], 
			baudrate=int(self.settings['baudrate']), 
			bytesize=int(self.settings['length']), 
			parity=self.settings['parity'], 
			stopbits=int(self.settings['stopbit']), 
			timeout=int(self.settings['timeout'])
		)


	def config(self):
		import configparser

		config = configparser.ConfigParser()
		config.read('settings.cfg')

		self.settings = {}
		for i in config['serialSettings']:
			self.settings[i] = config.get("serialSettings", i)

		self.variablesForGUI = {}
		for i in config['variables']:
			if (config.getboolean('variables', i)):
				self.variablesForGUI[i] = -1

		self.variablesForFH = {}
		for i in config['variables dict']:
			self.variablesForFH[i] = ast.literal_eval(config.get("variables dict", i))


	def decode(self, encodedMessage):

		if encodedMessage in [bytes([0x3F]) + b'ReadError', bytes([0x0A]) + b'ReadError', bytes([0x0A]) + b'ReadError']:
			
			return ['E', 'R', 'R', 'O', 'R', encodedMessage[0] & 0x3F]


		elif len(encodedMessage) % 4 != 1 or (encodedMessage == b'ReadError'):		#We receive a number of bytes multiple of 4, plus the byte which gives us the headerIndex of the block received
			
			return ['N', 'O', 'T', '%', '4']


		else:
			encodedMessage = list(encodedMessage)
			decodedMessage = []
			headerIndex=encodedMessage[0] & 0x3F
			decodedMessage.append(headerIndex)
			for i in range(0, len(encodedMessage)//4):
				firstByte = ((encodedMessage[4*i+1] & 0x3F)<<2 | (encodedMessage[4*i+2] & 0x3F)>>4) & 0xFF
				secondByte = ((encodedMessage[4*i+2] & 0x3F) << 4 | (encodedMessage[4*i+3] & 0x3F)>>2) & 0xFF
				thirdByte = ((encodedMessage[4*i+3] & 0x3F) << 6 | (encodedMessage[4*i+4] & 0x3F)) & 0xFF
				decodedMessage.append(firstByte)
				decodedMessage.append(secondByte)
				decodedMessage.append(thirdByte)
			
			return decodedMessage


	def formatData(self, encodedMessage):

		decodedMessage = self.decode(encodedMessage)

		if (decodedMessage[0]==0x3F):

			self.variablesForFH['engineframe']['rpm'] = int(decodedMessage[1]) << 8 | int(decodedMessage[2])

			self.variablesForFH['engineframe']["tps"] =  float(int(decodedMessage[3]) << 8 | int (decodedMessage[4])) / 10
			
			self.variablesForFH['gyroscope']["accel_x"] = float(int(decodedMessage[5]) << 8 | int (decodedMessage[6])) / 8192
			self.variablesForFH['gyroscope']["accel_y"] = float(int(decodedMessage[7]) << 8 | int (decodedMessage[8])) / 8192
			self.variablesForFH['gyroscope']["accel_z"] = float(int(decodedMessage[9]) << 8 | int (decodedMessage[10])) / 8192
			
			self.variablesForFH['gyroscope']["gyro_x"] = float(int(decodedMessage[11]) << 8 | int (decodedMessage[12])) / 8192
			self.variablesForFH['gyroscope']["gyro_y"] = float(int(decodedMessage[13]) << 8 | int (decodedMessage[14])) / 8192
			self.variablesForFH['gyroscope']["gyro_z"] = float(int(decodedMessage[15]) << 8 | int (decodedMessage[16])) / 8192

			#POTENTIOMETER'S OFFSET (THE NUMBER SUBTRACTED AT THE END OF THE LINE) MUST BE CALCULATED AT EVERY CAR'S TEST
			self.variablesForFH['wheelframe']["pot_fsx"] = (int(decodedMessage[17]) | ((int(decodedMessage[19]&0x0F))<<8))-610
			self.variablesForFH['wheelframe']["pot_fdx"] = (int(decodedMessage[18]) | ((int(decodedMessage[19]&0xF0))<<4))-410
			self.variablesForFH['wheelframe']["potFAccuracy"] = int(decodedMessage[20])
			self.variablesForFH['wheelframe']["pot_rsx"] = (int(decodedMessage[21]) | ((int(decodedMessage[23]&0x0F))<<8))-300
			self.variablesForFH['wheelframe']["pot_rdx"] = (int(decodedMessage[22]) | ((int(decodedMessage[23]&0xF0))<<4))-310
			self.variablesForFH['wheelframe']["potRAccuracy"] = int(decodedMessage[24])

			self.variablesForFH['wheelframe']["countFSx"] = (int(decodedMessage[27] & 0x0F) << 8) | int(decodedMessage[25])
			self.variablesForFH['wheelframe']["countFDx"] = (int(decodedMessage[27] & 0xF0) << 4) | int(decodedMessage[26])
			self.variablesForFH['wheelframe']["dtF"] = int(decodedMessage[28])
			
			# self.variablesForFH['wheelframe']["vel_fsx"] = SPEED_VALUE	# NOT IN USE (PHONIC WHEEL'S SPECS NOT AVAILABLE)
			# self.variablesForFH['wheelframe']["vel_fdx"] = SPEED_VALUE	# NOT IN USE (PHONIC WHEEL'S SPECS NOT AVAILABLE)
			
			self.variablesForFH['wheelframe']["countRSx"] = (int(decodedMessage[32] & 0x0F) << 8) | int(decodedMessage[30])
			self.variablesForFH['wheelframe']["countRDx"] = (int(decodedMessage[32] & 0xF0) << 4) | int(decodedMessage[31])
			self.variablesForFH['wheelframe']["dtR"] = int(decodedMessage[33])
			
			# self.variablesForFH['wheelframe']["vel_rsx"] = SPEED_VALUE	# NOT IN USE (PHONIC WHEEL'S SPECS NOT AVAILABLE)
			# self.variablesForFH['wheelframe']["vel_rdx"] = SPEED_VALUE	# NOT IN USE (PHONIC WHEEL'S SPECS NOT AVAILABLE)

			self.variablesForFH['engineframe']["gear"] = int(decodedMessage[34])


		elif (decodedMessage[0]==0x0A):

			self.variablesForFH['engineframe']["t_h20"] = int(decodedMessage[1]) -40
			self.variablesForFH['engineframe']["t_air"] = int(decodedMessage[2]) -40
			self.variablesForFH['engineframe']["t_oil"] = int(decodedMessage[3]) -40
			self.variablesForFH['engineframe']["vbb"] = (float(int(decodedMessage[4])))*0.0705
			self.variablesForFH['engineframe']["lambda1_avg"] = (float(int(decodedMessage[5])))/100
			self.variablesForFH['engineframe']["lambda1_raw"] = (float(int(decodedMessage[6])))/100
			self.variablesForFH['engineframe']["k_lambda1"] = (float(int(decodedMessage[7]) << 8 | int (decodedMessage[8])))/656
			self.variablesForFH['engineframe']["inj_low"] = (float(int(decodedMessage[9]) << 8 | int (decodedMessage[10])))/2
			self.variablesForFH['engineframe']["inj_high"] = (float(int(decodedMessage[11]) << 8 | int (decodedMessage[12])))/2


		elif(decodedMessage[0]==0x04):

			self.variablesForFH['gpsframe']["hour"] = int(decodedMessage[1])
			self.variablesForFH['gpsframe']["minutes"] = int(decodedMessage[2])
			self.variablesForFH['gpsframe']["seconds"] = int(decodedMessage[3])
			self.variablesForFH['gpsframe']["micro_seconds"] = (int(decodedMessage[4]) << 8) | (int(decodedMessage[5]))
			self.variablesForFH['gpsframe']["n_sats"] = int(decodedMessage[6] & 0x0F)
			self.variablesForFH['gpsframe']["fixQuality"] = int((decodedMessage[6] & 0x30) >> 4)

			e_w = int((decodedMessage[6] >> 6) & 0x01)
			if (e_w == 1):
				self.variablesForFH['gpsframe']["e_w"] = "E"
			else:
				self.variablesForFH['gpsframe']["e_w"] = "W"

			n_s = int(decodedMessage[6] >> 7)
			if (n_s == 1):
				self.variablesForFH['gpsframe']["n_s"] = "N"
			else:
				self.variablesForFH['gpsframe']["n_s"] = "S"

			self.variablesForFH['gpsframe']["hdop"] = int(decodedMessage[7] << 8) | int(decodedMessage[8])
			self.variablesForFH['gpsframe']["latitude"] = ((int(decodedMessage[9]) << 8) | int(decodedMessage[10])) + ((float((int(decodedMessage[11]) << 24) | (int(decodedMessage[12]) << 16) | (int(decodedMessage[13]) << 8) | int(decodedMessage[14]))) / 100000)
			self.variablesForFH['gpsframe']["longitude"] = ((int(decodedMessage[15]) << 24) | (int(decodedMessage[16]) << 16) | (int(decodedMessage[17]) << 8) | int(decodedMessage[18])) + ((float((int(decodedMessage[19]) << 24) | (int(decodedMessage[20]) << 16) | (int(decodedMessage[21]) << 8) | int(decodedMessage[22]))) / 100000)
			self.variablesForFH['gpsframe']["velGPS"] = float(decodedMessage[23]) + ((float(decodedMessage[23])) / 10)


		else:
			for i in self.variablesForFH:
				for j in self.variablesForFH[i]:
					self.variablesForFH[i][j] = 'Err'

		for i in self.variablesForGUI:
			for j in self.variablesForFH:
				if i in self.variablesForFH[j] :
					self.variablesForGUI[i] = self.variablesForFH[j][i]


	def readData(self):

		messageRead = bytes()


		if(self.serialInstance.in_waiting > 0):
			attempt = 0

			while True:

				charReceived = self.serialInstance.read(size=1)

				if charReceived == self.settings['startchar']:

					messageRead = self.serialInstance.read_until(self.settings['endchar'])[:-1]
					break


				elif attempt >= 200:
					return b'ReadError'


				else:
					attempt+=1

			self.formatData(messageRead)


	def sendData(self):

		self.FHPipeSerialEnd.send(self.variablesForFH)


		if (time.time() - self.lastGuiUpdate > 0.015):

			self.GuiPipeSerialEnd.send(self.variablesForGUI)
			self.lastGuiUpdate = time.time()


	def loop(self):

		self.serialInstance.reset_input_buffer()


		while True:

			self.readData()

			self.sendData()


"""
TODO:
deal with potentiometers offsets
"""

if __name__ == '__main__':
	import os

	bashCommand = "/usr/bin/env python3 ./launcher.py"
	os.system(bashCommand)
