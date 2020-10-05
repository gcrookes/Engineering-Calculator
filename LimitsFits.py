import tkinter as tk #0.2s import
from tkinter import ttk
from PIL import Image, ImageTk #0.06s import
#from EngineeringCalculator import StartPage

MID_FONT= ("Verdana", 12)
LARGE_FONT= ("Verdana", 16)


class LimitsFits(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		self.image = Image.open(r"LimitsFits.png")#image for the start menu button

		#Build two frames so you can look at the inside and outside of something if you want or multiple places on a shaft
		self.FrameLeft = self.LimitFrame("Shaft Size 1")
		self.FrameRight = self.LimitFrame("Shaft Size 2")
		self.FrameLeft.pack(side="left", fill="both", expand = 0,padx=10)
		self.FrameRight.pack(side="left", fill="both", expand =0,padx=10)

		#Add in the button to go back to the start menu
		tk.Button(self.FrameRight, text='Back to home', command=lambda: controller.show_frame('StartPage')).grid(row=100,column=3)

	def LimitFrame(self,title):
		#Build out the frames in a frame variable which is then returned
		frame = tk.Frame(self)
		row = 0

		#Title
		tk.Label(frame, text=title, font=LARGE_FONT).grid(row=row, columnspan=4)
		row+=1

		ttk.Separator(frame,orient=tk.HORIZONTAL).grid(row=row,columnspan=4,sticky='ew',pady=4)
		row+=1

		#Input box for the diameter
		tk.Label(frame, text="ϕ Nominal Diamter [mm]").grid(row=row,column=0, columnspan=2)
		frame.InputDiameter = tk.Entry(frame, validate='focusout', validatecommand=lambda:self.update(frame))
		frame.InputDiameter.grid(row=row, column=2, columnspan=2)
		frame.InputDiameter.bind("<Return>", lambda event: frame.focus_set()) #If you get rid of this line hitting enter in the input won't cause and update
		row+=1

		#Shaft and hole tolerance labels and combo box setup
		tk.Label(frame, text="Shaft:", font=MID_FONT).grid(row=row, column=0,sticky='W')
		tk.Label(frame, text="Hole:", font=MID_FONT).grid(row=row, column=2,sticky='W')


		frame.ShaftTolerance = ttk.Combobox(frame, validate='focusin', validatecommand=lambda:self.update(frame),width = 3)
		frame.HoleTolerance  = ttk.Combobox(frame, validate='focusin', validatecommand=lambda:self.update(frame),width = 3)
		frame.ShaftTolerance.grid(row=row, column=1, sticky='W',pady=10)
		frame.HoleTolerance.grid(row=row, column=3, sticky='W',pady=10)
		row+=1

		#Dump in the actual tolerance values
		frame.ShaftTolerance['values'] = ('b9','b11','c9','c11','d8','d9','d10','e7','e8','e9','f6','f7','f8','g5','g6','h5','h6','h7',
			'h8','h9','h10','js5','js6','js7','k5','k6','k7','m5','m6','m7','n5','n6','p5','p6','r6','s6','s7','t6','u6','u7','x6')
		frame.ShaftTolerance.current(18)#h8 is a decent tolerance value

		frame.HoleTolerance['values'] = ('B11','C10','C11','D9','D10','E8','E9','F7','F8','F9','G6','G7','H6','H7','H8','H9','H10','JS6',
			'JS7','K6','K7','M6','M7','N6','N7','P6','P7','R7','S7','T7','U7','X7')
		frame.HoleTolerance.current(14)#H8 is a decent tolerance value

		#Define labels
		labels = ['Nominal','Plus','Minus','Max','Min']
		frame.OutputShaft = {}
		frame.OutputHole = {}

		ttk.Separator(frame,orient=tk.HORIZONTAL).grid(row=row,columnspan=4,sticky='ew',pady=4)
		row+=1

		#Make the labels and entry boxes that need to be filled in.
		for label in labels:
			#Labels:
			tk.Label(frame, text=label).grid(row=row,column=0,sticky='E',padx=4)
			tk.Label(frame, text=label).grid(row=row,column=2,sticky='E',padx=4)

			#Boxes to show labels
			frame.OutputShaft[label] = tk.Entry(frame,justify='center',width=10)
			frame.OutputHole[label]  = tk.Entry(frame,justify='center',width=10)
			frame.OutputShaft[label].grid(row=row,column=1,sticky='W',padx=10)
			frame.OutputHole[label].grid(row=row,column=3,sticky='W',padx=10)
			row+=1

		ttk.Separator(frame,orient=tk.HORIZONTAL).grid(row=row,columnspan=4,sticky='ew',pady=4)
		row+=1

		#The final input boxes for overall clearance
		tk.Label(frame, text='Max Clearance').grid(row=row,column=0,sticky='E',padx=4)
		tk.Label(frame, text='Min Clearance').grid(row=row,column=2,sticky='E',padx=4)

		frame.MaxClearance = tk.Entry(frame,justify='center',width=10)
		frame.MinClearance = tk.Entry(frame,justify='center',width=10)
		frame.MaxClearance.grid(row=row,column=1,sticky='W',padx=10)
		frame.MinClearance.grid(row=row,column=3,sticky='W',padx=10)
		row+=1

		ttk.Separator(frame,orient=tk.HORIZONTAL).grid(row=row,columnspan=4,sticky='ew',pady=4)
		row+=1

		return frame



	def update(self, frame):

		#Make sure the entered value is actually a number, otherwise default back
		try:
			nominal = float(frame.InputDiameter.get())
		except:
			return 1

		#Pass the tolerance values into a different function and get back the upper and lower limits
		tolerances = self.ValueLookup(0,0,frame.HoleTolerance.get())

		#clear out values in the input boxes
		[box.delete(0,tk.END) for box in frame.OutputShaft.values()]
		[box.delete(0,tk.END) for box in frame.OutputHole.values()]
		frame.MaxClearance.delete(0,tk.END)
		frame.MinClearance.delete(0,tk.END)
		
		#Calculate the tolerances for the shaft and the hole
		shaft = {
			'Nominal':nominal, 
			'Plus':tolerances[0], 
			'Minus':tolerances[1], 
			'Max':nominal+tolerances[0], 
			'Min':nominal+tolerances[1]}

		hole = {
			'Nominal':nominal, 
			'Plus':tolerances[2], 
			'Minus':tolerances[3], 
			'Max':nominal+tolerances[2], 
			'Min':nominal+tolerances[3]}

		#Loop over all the output boxes and put in the correct values
		for label in shaft:
			frame.OutputShaft[label].insert(0,format(shaft[label],'0.3f'))
			frame.OutputHole[label].insert(0,format(hole[label],'0.3f'))

		#Calculate and return the min and max clearances
		frame.MaxClearance.insert(0,format(hole['Max']-shaft['Min'],'0.3f'))
		frame.MinClearance.insert(0,format(hole['Min']-shaft['Max'],'0.3f'))
		
		return 1


	def ValueLookup(self, Nominal, ShaftTolerance, HoleTolerance):

		#Need some actual code here to figure out the numbers based on the codes that get fed in
		results = ['Shaft Plus','Shaft Minus','Hole Plus','Hole Minus']
		results = [0.025,-0.03,0.05,-0.06] #Actually want to return the numbers with actual sign. Want them as floats not strings

		return results


if __name__ == '__main__':
	from EngineeringCalculator import EngineeringCalculator