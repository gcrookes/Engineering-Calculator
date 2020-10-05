import tkinter as tk #0.2s import
from tkinter import ttk
#import pandas as pd  #4.7s import
from PIL import Image, ImageTk #0.06s import
from LimitsFits import LimitsFits
SMALL_FONT= ("Verdana", 8)
MID_FONT= ("Verdana", 12)
LARGE_FONT= ("Verdana", 16)

class EngineeringCalculator(tk.Tk):

	def __init__(self, *args, **kwargs):
		
		#Initialize window, title, icon
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("Mechinical Engineering Calculator")
		self.iconbitmap(default=r"Gears.ico")

		#Main frame
		container = tk.Frame(self)

		#Pack the main frame into the window
		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#This is the main list of functions the buttons and programs are built on. The key is what will show up on the button and the value is the class that it calls
		#To add a new function you have to copy the bummy frame class and rename it, then update the values here. The window that shows up on the screen can then be
		#build up in the initialize funtion of the class
		self.Pages = {
			'Limits and Fits':LimitsFits,
			'Placeholder 2':DummyFrame,
			'Placeholder 3':DummyFrame,
			'Placeholder 4':DummyFrame,
			'Placeholder 5':DummyFrame,
			'Placeholder 6':DummyFrame,
			'Placeholder 7':DummyFrame,
			'Placeholder 8':DummyFrame,
			'Placeholder 9':DummyFrame,
			'Placeholder 10':DummyFrame,
			'Placeholder 11':DummyFrame,
			'Placeholder 12':DummyFrame,
			'Placeholder 13':DummyFrame,
			'Placeholder 14':DummyFrame,
			'Placeholder 15':DummyFrame,
			'Placeholder 16':DummyFrame,
			'Placeholder 17':DummyFrame,
			'Placeholder 18':DummyFrame,
			'Placeholder 19':DummyFrame,
			'Placeholder 20':DummyFrame,
			}

		#Set up the sub frames that are brought up for each new page
		self.frames = {}

		#Build an object for each of the different functions and store it in a list called self.frames
		for F in self.Pages.values():
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		#Then add the start page, this is not in the Pages dictionary so that it does not need to be filtered out of the buttons
		self.frames['StartPage'] = StartPage(container,self)
		self.frames['StartPage'].grid(row=0, column=0, sticky="nsew")

		#Show the initial frame
		self.show_frame('StartPage')
		
		#bring up a different frame off the bat for development
		#self.show_frame(LimitsFits)

	def show_frame(self, cont):
		# Raise the selected frame to be shown.
		frame = self.frames[cont]
		frame.tkraise()


class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)

		#Initialization to determine how the rows show up
		count = 0
		row = 0
		col = 0
		ColumnsPerRow = 5
		self.ButtonSize = 120
		Pading = 10

		self.ims = {}

		for page in controller.Pages:
			#Sorting into rows with logic, this might be overkill
			row = int(count/ColumnsPerRow)
			col = count % ColumnsPerRow
			count +=1

			#resize the image stored in each object and set it up to go on a button
			icon = controller.frames[controller.Pages[page]].image.resize((int(self.ButtonSize*0.9), int(self.ButtonSize*0.9*0.75)), Image.ANTIALIAS)
			icon = ImageTk.PhotoImage(icon)

			#Building up the buttons
			#The command is a lambda function so I can pass a variable. the i=...: part is so that it captures the current page, otherwise it will use the final page when the for loop is done
			b = tk.Button(self, text=page, command=lambda i=controller.Pages[page]: controller.show_frame(i))
			#Slap the icon on and do some other formatting. compound is where the image will be displayed
			b.configure(image=icon,compound = tk.TOP, width = self.ButtonSize, height = self.ButtonSize, font = MID_FONT)
			#Actually pack the button onto the grid
			b.grid(row=row,column=col,padx=Pading, pady=Pading)

			#Jenky shit but I have to store the icon somewhere or pyton clears it from memory. If I store it back into the original object which would be prefered it only works for the images 
			#that are not dummy. Could save into the object if they are all distinct classes.
			self.ims[page]=icon


class DummyFrame(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		self.image = Image.open(r"DummyFrame.png")#image for the start menu button


app = EngineeringCalculator()
app.mainloop()