import configparser
import ast
import tkinter as tk

width=1920
height=1080

config = configparser.ConfigParser()
config.read('settings.cfg')

settings = {}
for i in config['serialSettings']:
	settings[i] = config.get("serialSettings", i)

variablesForGUI = {}
for i in config['variables']:
	if (config.getboolean('variables', i)):
		variablesForGUI[i] = -1

variablesForFH = {}
for i in config['variables dict']:
	variablesForFH[i] = ast.literal_eval(config.get("variables dict", i))



print(variablesForGUI)

root = tk.Tk()
root.withdraw()
root.attributes("-fullscreen", True)
root.overrideredirect(True)