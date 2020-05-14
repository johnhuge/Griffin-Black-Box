#! /usr/bin/env python3

if __name__ == 'fileHandler':
	import time
	import csv
	import ast


class FileHandler:


	def __init__(self, FHPipeFHEnd):

		self.FHPipeFHEnd = FHPipeFHEnd

		self.lastTime100 = self.lastTime10 = self.lastTime4 = time.time()

		self.config()

		prefix = "logs/" + time.strftime("%a_%d_%b_%Y") + " " + time.strftime("%H_%M_%S_")

		self.createFile100(prefix)
		
		self.createFile10(prefix)

		self.createFile4(prefix)


	def config(self):
		import configparser

		config = configparser.ConfigParser()
		config.read("settings.cfg")
		
		self.variables = {}
		for i in config['variables dict']:
			self.variables[i] = ast.literal_eval(config.get("variables dict", i))


	def createFile100(self, prefix):

		self.__name100Hz = prefix + "100Hz.csv"

		__fieldnames100Hz = ['rpm', 'tps', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'pot_fsx',  'pot_fdx', 'pot_FAccuracy', 'pot_rsx',  'pot_rdx', 'pot_RAccuracy','steeringEncoder', 'vel_fsx', 'vel_fdx', 'vel_rsx', 'vel_rdx', 'gear']

		self.__file100Hz = open(self.__name100Hz, 'w', newline='')
		self.__writerFile100Hz = csv.writer(self.__file100Hz, delimiter=',', dialect='excel')
		self.__writerFile100Hz.writerow(__fieldnames100Hz)
		self.__lineNumber100Hz = 1


	def createFile10(self, prefix):
		
		self.__name10Hz = prefix + "10Hz.csv"

		__fieldnames10Hz = ['t_h20', 't_air', 't_oil', 'vbb', 'lambda1_avg', 'lambda1_raw', 'k_lambda1', 'inj_low', 'inj_high']

		self.__file10Hz = open(self.__name10Hz, 'w', newline='')
		self.__writerFile10Hz = csv.writer(self.__file10Hz, delimiter=',', dialect='excel')
		self.__writerFile10Hz.writerow(__fieldnames10Hz)
		self.__lineNumber10Hz = 1


	def createFile4(self, prefix):
		
		self.__name4Hz = prefix + "4Hz.csv"

		__fieldnames4Hz = ['hour', 'minutes', 'seconds', 'micro_seconds', 'n_sats', 'fixQuality', 'e_w', 'n_s', 'hdop', 'latitude', 'longitude', 'velGPS']

		self.__file4Hz = open(self.__name4Hz, 'w', newline='')
		self.__writerFile4Hz = csv.writer(self.__file4Hz, delimiter=',', dialect='excel')
		self.__writerFile4Hz.writerow(__fieldnames4Hz)
		self.__lineNumber4Hz = 1


	def writeFile100(self):

		FrameValues100Hz = []

		FrameValues100Hz.append(self.variables['engineframe']["rpm"])
		FrameValues100Hz.append(self.variables['engineframe']["tps"])
		FrameValues100Hz.append(self.variables['gyroscope']['accel_x'])
		FrameValues100Hz.append(self.variables['gyroscope']['accel_y'])
		FrameValues100Hz.append(self.variables['gyroscope']['accel_z'])
		FrameValues100Hz.append(self.variables['gyroscope']['gyro_x'])
		FrameValues100Hz.append(self.variables['gyroscope']['gyro_y'])
		FrameValues100Hz.append(self.variables['gyroscope']['gyro_z'])
		FrameValues100Hz.append(self.variables['wheelframe']['pot_fsx'])
		FrameValues100Hz.append(self.variables['wheelframe']['pot_fdx'])
		FrameValues100Hz.append(self.variables['wheelframe']['potFAccuracy'])
		FrameValues100Hz.append(self.variables['wheelframe']['pot_rsx'])
		FrameValues100Hz.append(self.variables['wheelframe']['pot_rdx'])
		FrameValues100Hz.append(self.variables['wheelframe']['potRAccuracy'])
		FrameValues100Hz.append(self.variables['wheelframe']['steeringEncoder'])
		FrameValues100Hz.append(self.variables['wheelframe']['vel_fsx'])
		FrameValues100Hz.append(self.variables['wheelframe']['vel_fdx'])
		FrameValues100Hz.append(self.variables['wheelframe']['vel_rsx'])
		FrameValues100Hz.append(self.variables['wheelframe']['vel_rdx'])
		FrameValues100Hz.append(self.variables['engineframe']['gear'])

		self.__writerFile100Hz.writerow(FrameValues100Hz)


		# CLOSES THE FILE EVERY 500 WRITINGS
		self.__lineNumber100Hz = (self.__lineNumber100Hz + 1) % 500


		if (self.__lineNumber100Hz==0):

			self.__file100Hz.close()
			self.__file100Hz = open(self.__name100Hz, 'a', newline='')
			self.__writerFile100Hz = csv.writer(self.__file100Hz, delimiter=',', dialect='excel')


	def writeFile10(self):

		FrameValues10Hz = []

		FrameValues10Hz.append(self.variables['engineframe']["t_h20"])     
		FrameValues10Hz.append(self.variables['engineframe']["t_air"])
		FrameValues10Hz.append(self.variables['engineframe']["t_oil"])
		FrameValues10Hz.append(self.variables['engineframe']["vbb"])
		FrameValues10Hz.append(self.variables['engineframe']["lambda1_avg"])
		FrameValues10Hz.append(self.variables['engineframe']["lambda1_raw"])
		FrameValues10Hz.append(self.variables['engineframe']["k_lambda1"])
		FrameValues10Hz.append(self.variables['engineframe']["inj_low"])
		FrameValues10Hz.append(self.variables['engineframe']["inj_high"])

		self.__writerFile10Hz.writerow(FrameValues10Hz)
		

		# CLOSES THE FILE EVERY 50 WRITINGS
		self.__lineNumber10Hz = (self.__lineNumber10Hz + 1) % 50


		if (self.__lineNumber10Hz==0):

			self.__file10Hz.close()
			self.__file10Hz = open(self.__name10Hz, 'a', newline='')
			self.__writerFile10Hz = csv.writer(self.__file10Hz, delimiter=',', dialect='excel')


	def writeFile4(self):

		FrameValues4Hz = []

		FrameValues4Hz.append(self. variables['gpsframe']['hour'])
		FrameValues4Hz.append(self. variables['gpsframe']['minutes'])
		FrameValues4Hz.append(self. variables['gpsframe']['seconds'])
		FrameValues4Hz.append(self. variables['gpsframe']['micro_seconds'])
		FrameValues4Hz.append(self. variables['gpsframe']['n_sats'])
		FrameValues4Hz.append(self. variables['gpsframe']['fixQuality'])
		FrameValues4Hz.append(self. variables['gpsframe']['e_w'])
		FrameValues4Hz.append(self. variables['gpsframe']['n_s'])
		FrameValues4Hz.append(self. variables['gpsframe']['hdop'])
		FrameValues4Hz.append(self. variables['gpsframe']['latitude'])
		FrameValues4Hz.append(self. variables['gpsframe']['longitude'])
		FrameValues4Hz.append(self. variables['gpsframe']['velGPS'])

		self.__writerFile4Hz.writerow(FrameValues4Hz)


		# CLOSES THE FILE EVERY 20 WRITINGS
		self.__lineNumber4Hz = (self.__lineNumber4Hz + 1) % 20


		if (self.__lineNumber4Hz==0):

			self.__file4Hz.close()
			self.__file4Hz = open(self.__name4Hz, 'a', newline='')
			self.__writerFile4Hz = csv.writer(self.__file4Hz, delimiter=',', dialect='excel')


	def loop(self):

		while True:

			# waits 10ms for new data
			if self.FHPipeFHEnd.poll(0.01):

				self.variables = self.FHPipeFHEnd.recv()

				self.lastTimeAssignment = time.time()

			# if there is no new data, data is set to 'timeout'
			else:

				for i in self.variables:
					for j in self.variables[i]:
						self.variables[i][j] = 'timeout'

				self.lastTimeAssignment = time.time()

			# logs 100 times per second
			if self.lastTimeAssignment - self.lastTime100 >= 0.01:

				self.lastTime100 = self.lastTimeAssignment

				self.writeFile100()

			# logs 10 times per second
			if self.lastTimeAssignment - self.lastTime10 >= 0.1:

				self.lastTime10 = self.lastTimeAssignment

				self.writeFile10()

			# logs 4 times per second
			if self.lastTimeAssignment - self.lastTime4 >= 0.25:

				self.lastTime4 = self.lastTimeAssignment

				self.writeFile4()




if __name__ == '__main__':
	bashCommand = "/usr/bin/env python3 ./launcher.py"
	import os
	os.system(bashCommand)
