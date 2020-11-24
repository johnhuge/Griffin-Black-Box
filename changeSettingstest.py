import tkinter as tk
from tkinter import ttk
import time
import configparser
import codecs
from PIL import Image, ImageTk
import ast

class ChangeSettings():
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		filename = self.config.read("settings.cfg")

		self.width=800
		self.height=480

		self.mainWindow = tk.Tk()
		self.mainWindow.geometry(str(self.width)+'x'+str(self.height))
		# self.mainWindow.withdraw()
		# self.mainWindow.attributes("-fullscreen", True)
		self.mainWindow.overrideredirect(True)

		self.root = ttk.Frame(self.mainWindow, width=self.width, height=self.height)
		self.root.pack(anchor='w')

		self.variables = {}

		for i in self.config['variables']:
			self.variables[i] = tk.BooleanVar()
			self.variables[i].set(self.config.getboolean('variables', i))

		count = 0
		self.checkbuttons=[]
		for i in self.variables:
			self.checkbuttons.append(tk.Checkbutton(self.root,
				text=i, 
				takefocus = 1, 
				justify = "left", 
				onvalue=True, 
				offvalue=False, 
				variable=self.variables[i], 
				# command=lambda: placeLabel(i),
				state='disabled' if 'rpm' in i or 'vel_' in i else 'normal'
				))
			self.checkbuttons[-1].grid(
				column = count//6+1, 
				row= count % 6, 
				sticky = 'w'
				)
			self.checkbuttons[-1].bind("<Button-1>", lambda e: self.placeLabel(e))
			self.root.columnconfigure(count//6, weight=1, minsize=self.width/6)
			self.root.rowconfigure(count%6, weight=1, minsize=self.height/6)
			count += 1


		self.leftrect=tk.StringVar()
		self.leftrect.set(self.config.get('rects', 'left'))
		self.rightrect=tk.StringVar()
		self.rightrect.set(self.config.get('rects', 'right'))

		self.frame = ttk.Frame(self.root, borderwidth=5, relief="sunken")
		# self.frame.pack(side='right', anchor='n', fill=tk.Y)
		self.frame.grid(column=6, row=0, rowspan=6)
		self.root.columnconfigure(0, weight=1, minsize=self.width/12)
		self.root.columnconfigure(5, weight=1, minsize=self.width/6)
		self.root.columnconfigure(6, weight=1, minsize=self.width/6)
		self.root.rowconfigure(count%6, weight=1, minsize=self.height/6)						

		rectvalues = []
		for i in self.config['variables']:
			rectvalues.append(i)


		tk.Label(self.frame, text='').pack()

		tk.Label(self.frame, text='Left Rect:').pack(anchor='w', padx=6)
		ttk.Combobox(self.frame, values= rectvalues, textvariable=self.leftrect, state='readonly').pack(padx=10)
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()

		tk.Label(self.frame, text='Right Rect:').pack(anchor='w', padx=6)
		ttk.Combobox(self.frame, values= rectvalues, textvariable=self.rightrect, state='readonly').pack(padx=10)
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()
		tk.Label(self.frame, text='').pack()


		tk.Button(self.frame, text='Save and quit', command=self.save).pack(side='bottom', pady=3)
		tk.Button(self.frame, text='Discard changes and quit', command=self.mainWindow.destroy).pack(side='bottom', pady=3)

		# placeLabel('')
		self.mainWindow.deiconify()
		self.mainWindow.lift()


	def save(self):
		for i in self.variables:
			self.config.set('variables', str(i), str(self.variables[i].get()))
		self.config.set('rects', 'right', self.rightrect.get())
		self.config.set('rects', 'left', self.leftrect.get())
		with open("settings.cfg", 'w') as f:
			self.config.write(f)
		self.mainWindow.destroy()

	def placeLabel(self, event):
		# event.widget.toggle()
		print(event.widget)
		# print(event.widget.cget("state"))
		# print(self.variables[event.widget.cget('text')].get())
		if event.widget.cget("state") == 'disbled' or self.variables[event.widget.cget('text')].get(): 			#controsenso: nel momento in cui clicchi il checkbutton lui ha il valore di prima che tu lo cliccassi
			return
		self.cockpitFrame = ttk.Frame(self.mainWindow)
		self.cockpitFrame.place(x=0, y=0)
		self.img=Image.open('MiniCockpit.png')
		self.photo=ImageTk.PhotoImage(self.img)
		self.cockpitLabel = tk.Label(self.cockpitFrame, image = self.photo)
		self.cockpitLabel.image = self.photo
		self.cockpitLabel.pack()

		# aggiungi le posizioni di tutte le variabili
		self.initialPos=ast.literal_eval(self.config.get('widgets position', event.widget.cget('text'))) 
		print(self.initialPos)

		widget = tk.Label(self.cockpitFrame, text=event.widget.cget('text'))
		widget.place(x=self.initialPos['x'], y=self.initialPos['y'])
		widget.config(font=("Courier", 24))
		# widget.place(x=100, y=100)

		self.savePosButton = tk.Button(self.cockpitFrame, text='save position', command=lambda: self.savePosition(widget = widget, checkbutton=event.widget))
		self.savePosButton.place(x=0, y=0)

		self.cockpitLabel.bind("<Button-1>", lambda e: self.on_drag_start(e,widget = widget))
		self.cockpitLabel.bind("<B1-Motion>", lambda e: self.on_drag_motion(e,widget = widget))
		widget.bind("<Button-1>", lambda e: self.on_drag_start(e,widget=widget))
		widget.bind("<B1-Motion>", lambda e: self.on_drag_motion(e,widget=widget))
		# self.cockpitFrame.place_forget()
		# self.cockpitFrame.place(x=0, y=0)
		# event.widget.select()

	def savePosition(self, checkbutton, widget):
		checkbutton.select()		#<-----------------		pare funzioni ma non ci giurerei


		print(str(widget.winfo_x()))
		self.config.set('widgets position', widget.cget('text'), """{
		'x' : """ +str(widget.winfo_x())+ """,
		'y' : """ +str(widget.winfo_y())+ """
		}""")
		with open("settings.cfg", 'w') as f:
			self.config.write(f)
		self.cockpitFrame.place_forget()
		# pass

	def on_drag_start(self, event, widget):
		widget._drag_start_x = event.x
		widget._drag_start_y = event.y

	def on_drag_motion(self, event, widget):
		x = widget.winfo_x() - widget._drag_start_x + event.x
		y = widget.winfo_y() - widget._drag_start_y + event.y
		if event.widget.winfo_x() == 0:
			widget._drag_start_x = event.x
			widget._drag_start_y = event.y
		widget.place(x=x, y=y)


	def main(self):
		self.mainWindow.deiconify()
		self.mainWindow.lift()
		self.mainWindow.attributes("-topmost", True)		#altrimenti la finestra si apre in background
		# self.mainWindow.attributes("-topmost", False)
		self.mainWindow.mainloop()