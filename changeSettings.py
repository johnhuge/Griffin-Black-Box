import tkinter as tk
from tkinter import ttk
import time
import configparser
import codecs
from PIL import Image, ImageTk
import ast

class ChangeSettings():
	
	def __init__(self):
		config = configparser.ConfigParser()
		filename = config.read("settings.cfg")

		width=800
		height=480

		mainWindow = tk.Tk()
		mainWindow.geometry(str(width)+'x'+str(height))
		mainWindow.withdraw()
		# mainWindow.attributes("-fullscreen", True)
		mainWindow.overrideredirect(True)

		root = ttk.Frame(mainWindow, width=width, height=height)
		root.pack(anchor='w')

		variables = {}

		for i in config['variables']:
			variables[i] = tk.BooleanVar()
			variables[i].set(config.getboolean('variables', i))

		count = 0
		checkbuttons=[]
		for i in variables:
			checkbuttons.append(tk.Checkbutton(root,
				text=i, 
				takefocus = 1, 
				justify = "left", 
				onvalue=True, 
				offvalue=False, 
				variable=variables[i], 
				# command=lambda: placeLabel(i),
				state='disabled' if 'rpm' in i or 'vel_' in i else 'normal'
				))
			checkbuttons[-1].grid(
				column = count//6+1, 
				row= count % 6, 
				sticky = 'w'
				)
			checkbuttons[-1].bind("<Button-1>", lambda e: placeLabel(e))
			root.columnconfigure(count//6, weight=1, minsize=width/6)
			root.rowconfigure(count%6, weight=1, minsize=height/6)
			count += 1


		leftrect=tk.StringVar()
		leftrect.set(config.get('rects', 'left'))
		rightrect=tk.StringVar()
		rightrect.set(config.get('rects', 'right'))

		frame = ttk.Frame(root, borderwidth=5, relief="sunken")
		# frame.pack(side='right', anchor='n', fill=tk.Y)
		frame.grid(column=6, row=0, rowspan=6)
		root.columnconfigure(0, weight=1, minsize=width/12)
		root.columnconfigure(5, weight=1, minsize=width/6)
		root.columnconfigure(6, weight=1, minsize=width/6)
		root.rowconfigure(count%6, weight=1, minsize=height/6)						

		rectvalues = []
		for i in config['variables']:
			rectvalues.append(i)


		tk.Label(frame, text='').pack()

		tk.Label(frame, text='Left Rect:').pack(anchor='w', padx=6)
		ttk.Combobox(frame, values= rectvalues, textvariable=leftrect, state='readonly').pack(padx=10)
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()

		tk.Label(frame, text='Right Rect:').pack(anchor='w', padx=6)
		ttk.Combobox(frame, values= rectvalues, textvariable=rightrect, state='readonly').pack(padx=10)
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()
		tk.Label(frame, text='').pack()


		tk.Button(frame, text='SAVE', command=save).pack(side='bottom', pady=10)

		# placeLabel('')

	def save():
		for i in variables:
			config.set('variables', str(i), str(variables[i].get()))
		config.set('rects', 'right', rightrect.get())
		config.set('rects', 'left', leftrect.get())
		with open("settings.cfg", 'w') as f:
			config.write(f)
		mainWindow.destroy()

	def placeLabel(event):
		# event.widget.toggle()
		print(event.widget)
		# print(event.widget.cget("state"))
		# print(variables[event.widget.cget('text')].get())
		if event.widget.cget("state") == 'disbled' or variables[event.widget.cget('text')].get(): 			#controsenso: nel momento in cui clicchi il checkbutton lui ha il valore di prima che tu lo cliccassi
			return
		cockpitFrame = ttk.Frame(mainWindow)
		cockpitFrame.place(x=0, y=0)
		img=Image.open('MiniCockpit.png')
		photo=ImageTk.PhotoImage(img)
		cockpitLabel = tk.Label(cockpitFrame, image = photo)
		cockpitLabel.image = photo
		cockpitLabel.pack()

		# aggiungi le posizioni di tutte le variabili
		initialPos=ast.literal_eval(config.get('widgets position', event.widget.cget('text'))) 
		print(initialPos)

		widget = tk.Label(cockpitFrame, text=event.widget.cget('text'))
		widget.place(x=initialPos['x'], y=initialPos['y'])
		widget.config(font=("Courier", 24))
		# widget.place(x=100, y=100)

		savePosButton = tk.Button(cockpitFrame, text='save position', command=lambda: savePosition(cockpitFrame, widget = widget, checkbutton=event.widget))
		savePosButton.place(x=0, y=0)

		cockpitLabel.bind("<Button-1>", lambda e: on_drag_start(e,widget = widget))
		cockpitLabel.bind("<B1-Motion>", lambda e: on_drag_motion(e,widget = widget))
		widget.bind("<Button-1>", lambda e: on_drag_start(e,widget=widget))
		widget.bind("<B1-Motion>", lambda e: on_drag_motion(e,widget=widget))
		# cockpitFrame.place_forget()
		# cockpitFrame.place(x=0, y=0)
		# event.widget.select()

	def savePosition(cockpitFrame, checkbutton, widget):
		checkbutton.select()		#<-----------------		pare funzioni ma non ci giurerei


		print(str(widget.winfo_x()))
		config.set('widgets position', widget.cget('text'), """{
		'x' : """ +str(widget.winfo_x())+ """,
		'y' : """ +str(widget.winfo_y())+ """
		}""")
		with open("settings.cfg", 'w') as f:
			config.write(f)
		cockpitFrame.place_forget()
		# pass

	def on_drag_start(event, widget):
		widget._drag_start_x = event.x
		widget._drag_start_y = event.y

	def on_drag_motion(event, widget):
		x = widget.winfo_x() - widget._drag_start_x + event.x
		y = widget.winfo_y() - widget._drag_start_y + event.y
		if event.widget.winfo_x() == 0:
			widget._drag_start_x = event.x
			widget._drag_start_y = event.y
		widget.place(x=x, y=y)


	def main(self):
		mainWindow.deiconify()
		mainWindow.lift()
		mainWindow.mainloop()