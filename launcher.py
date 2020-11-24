#! /usr/bin/env python3

# class Process(multiprocessing.Process):
#     def __init__(self, *args, **kwargs):
#         multiprocessing.Process.__init__(self, *args, **kwargs)
#         self._pconn, self._cconn = multiprocessing.Pipe()
#         self._exception = None

#     def run(self):
#         try:
#             multiprocessing.Process.run(self)
#             self._cconn.send(None)
#         except Exception as e:
#             tb = traceback.format_exc()
#             self._cconn.send((e, tb))
#             # raise e  # You can still rise this exception if you need to

#     @property
#     def exception(self):
#         if self._pconn.poll():
#             self._exception = self._pconn.recv()
#         return self._exception

def createDefaultCfg(): 
	
	with open('settings.cfg', 'w') as f:
		f.write(
'''[video settings]
width = 800
height = 480

[variables]
rpm = true
tps = false
t_h20 = true
t_air = false
t_oil = false
vbb = false
lambda1_avg = false
lambda1_raw = false
k_lambda1 = false
inj_low = false
inj_high = false
gear = true
velGPS = false
vel_fsx = true
vel_fdx = true
vel_rsx = true
vel_rdx = true

[rects]
left = t_h20
right = tps

[absolute max]
rpm = 12500
t_h20 = 120
vbb = 14.7

[serialSettings]
name = /dev/ttyUSB0
baudrate = 115200
stopBit = 1
length = 8
parity = N
timeout = 192 
#timeout = baudrate/600
bytesToRead = 1
startChar = \\x02
endChar = \\x03

[variables dict]
engineFrame = {
	'rpm' : -1,
	'tps' : -1,
	't_h20' : -1,
	't_air' : -1,
	't_oil' : -1,
	'vbb' : -1,
	'lambda1_avg' : -1,
	'lambda1_raw' : -1,
	'k_lambda1' : -1,
	'inj_low' : -1,
	'inj_high' : -1,
	'gear' : -1
	}
gpsFrame = {
	'hour' : -1,
	'minutes' : -1,
	'seconds' : -1,
	'micro_seconds' : -1,
	'n_s' : -1,
	'e_w' : -1,
	'fixQuality' : -1,
	'n_sats' : -1,
	'hdop' : -1,
	'latitude' : -1,
	'longitude' : -1,
	'velGPS' : -1
	}
wheelFrame = {
	'vel_fsx' : -1,
	'vel_fdx' : -1,
	'vel_rsx' : -1,
	'vel_rdx' : -1,
	'pot_fdx' : -1,
	'pot_fsx' : -1,
	'pot_rdx' : -1,
	'pot_rsx' : -1,
	'potFAccuracy' : -1,
	'potRAccuracy' : -1,
	'steeringEncoder' : -1,
	'dtF' : -1,
	'dtR' : -1,
	'countRSx' : -1,
	'countRDx' : -1
	}
gyroscope = {
	'gyro_x' : -1,
	'gyro_y' : -1,
	'gyro_z' : -1,
	'accel_x' : -1,
	'accel_y' : -1,
	'accel_z' : -1
	}
'''
			)


def createLogsFolder():
	
	os.mkdir('logs')


def startSerial(GuiPipeSerialEnd, FHPipeSerialEnd):
	import serialHandler

	serialHandler.SerialHandler(GuiPipeSerialEnd, FHPipeSerialEnd).loop()


def startFH(FHPipeFHEnd):
	import fileHandler

	fileHandler.FileHandler(FHPipeFHEnd).loop()


def startGui(GuiPipeGuiEnd):
	import gui

	gui.Gui(GuiPipeGuiEnd).loop()


def main():

	if not os.path.exists('settings.cfg'):
		createDefaultCfg()

	if not os.path.exists('logs/'):
		createLogsFolder()


	GuiPipeGuiEnd, GuiPipeSerialEnd = multiprocessing.Pipe()
	FHPipeFHEnd, FHPipeSerialEnd = multiprocessing.Pipe()

	SHProcess = Process.Process(target=startSerial, daemon = True, name = "__SHProcess__", args=(GuiPipeSerialEnd, FHPipeSerialEnd))
	FHProcess = Process.Process(target=startFH, daemon = True, name = "__FHProcess__", args=(FHPipeFHEnd,))
	GuiProcess = Process.Process(target=startGui, daemon = True, name = "__GuiProcess__", args=(GuiPipeGuiEnd,))

	SHProcess.start()
	FHProcess.start()

	while True:
		GuiProcess.start()
		GuiProcess.join()

		if GuiProcess.exception:
			error, traceback = GuiProcess.exception
			print(error)
			print(traceback)

			if str(error) == 'accessing settings':
				print('okay modifichiamo')
				changeSettingsInstance = changeSettingstest.ChangeSettings()
				changeSettingsInstance.main()
				GuiProcess = Process.Process(target=startGui, daemon = True, name = "__GuiProcess__", args=(GuiPipeGuiEnd,))

			else:
				return
		else:
			return



if __name__ == '__main__':
	import multiprocessing
	import Process
	import os
	import changeSettingstest

	main()

if __name__ == 'launcher':
	import multiprocessing
	import Process
	import os
	import changeSettingstest

	main()
