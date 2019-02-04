from tkinter import*
import tkinter.messagebox
import json



def donothing():
    print("Nothing is to be done")
	
def equalizer_window():
	root = Tk()
	root.minsize(250, 100)
	with open("equi.txt", "r") as file:
	    music_data = json.load(file)
	root.title("Equalizer ")
	drop_menu = Menu(root)
	root.config(menu=drop_menu, bd=1, relief=RAISED)

	submenu = Menu(drop_menu, tearoff=0)
	drop_menu.add_cascade(label="Set Equalizer", menu=submenu)

	for preset in music_data:
	    submenu.add_command(label=preset["Name"], command = donothing)


	scale_frame = Frame(root)
	scale_frame.pack(side=TOP)

	scale_1 = Scale(scale_frame)
	scale_1.set(50)
	scale_1.pack(side=LEFT, padx=2)

	scale_2 = Scale(scale_frame)
	scale_2.set(50)
	scale_2.pack(side=LEFT, padx=2)

	scale_3 = Scale(scale_frame)
	scale_3.set(50)
	scale_3.pack(side=LEFT, padx=2)

	scale_4 = Scale(scale_frame)
	scale_4.set(50)
	scale_4.pack(side=LEFT, padx=2)

	scale_5 = Scale(scale_frame)
	scale_5.set(50)
	scale_5.pack(side=LEFT, padx=2)

	scale_6 = Scale(scale_frame)
	scale_6.set(50)
	scale_6.pack(side=LEFT, padx=2)

	label_frame = Frame(root)
	label_frame.pack(side=BOTTOM, padx=2)

	lazy_spacing = Label(label_frame, text="     ")
	lazy_spacing.pack(side=LEFT)

	label_1 = Label(label_frame, text='Bass')
	label_1.pack(side=LEFT, padx=2)
	label_2 = Label(label_frame, text='          ')
	label_2.pack(side=LEFT, padx=2)
	label_3 = Label(label_frame, text='          ')
	label_3.pack(side=LEFT, padx=2)
	label_4 = Label(label_frame, text='          ')
	label_4.pack(side=LEFT, padx=2)
	label_5 = Label(label_frame, text='          ')
	label_5.pack(side=LEFT, padx=2)
	label_6 = Label(label_frame, text='Treble')
	label_6.pack(side=LEFT, padx=2)


