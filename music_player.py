import os
from tkinter.filedialog import askdirectory

import pygame
from tkinter import *
import tkinter.messagebox

listofsongs = []
index = 0
count = 0
volume = 0.8
muted = False

root = Tk()
root.minsize(300,250)

pygame.mixer.init()

def about_us():
    tkinter.messagebox.showinfo('About Us', 'We are a group of friends making a music player')

def directorychooser():
    global count
    global directory
    count = 0
    directory = askdirectory()
    os.chdir(directory)
 
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            listofsongs.append(files)
            count += 1
    update_list()
    pygame.mixer.music.load(listofsongs[0])

def update_list():
    listofsongs.reverse()
    for items in listofsongs:
        listbox.insert(0,items)     
    listofsongs.reverse()

def update_display():
    global index
    displaybox.insert(0, listofsongs[index])

def updatelabel():
    global index
    global songname
    root.title("Music Player: "+ listofsongs[index])
    v.set(listofsongs[index])
    
def prevsong(event):
    try:
        global index
        if index == 0:
            index = (count - 1)
        else:
            index -= 1
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        statusbar['text'] = "Playing: "+ listofsongs[index]
        updatelabel()
        update_display()
    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')

def playsong(event):
    global index
    global paused
    global muted
    try:
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        statusbar['text'] = "Playing: "+ listofsongs[index]
        paused = False
        muted = False
        updatelabel()
        update_display()
    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')


def pausesong(event):
    global index
    global paused
    pygame.mixer.music.load(listofsongs[index])
    if paused:
        pygame.mixer.music.unpause()
        pausebutton.configure(image = pause_button)
        statusbar['text'] = "Playing: "+ listofsongs[index]
        paused = False
    else:
        pygame.mixer.music.pause()
        pausebutton.configure(image = play_button)
        statusbar['text'] = "Paused: "+ listofsongs[index]
        paused = True

def nextsong(event):
    try:
        global index
        index = (index + 1) % count
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        statusbar['text'] = "Playing: "+ listofsongs[index]
        updatelabel()
        update_display()
    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')

def stopsong(event):
    pygame.mixer.music.stop()
    statusbar['text'] = "Stoped playing: "+ listofsongs[index]
    v.set("")

def set_vol(val):
    global volume
    volume = int(val) / 100
    pygame.mixer.music.set_volume(volume)

def mute_music(event):
    global muted
    global initial_volume
    if muted:#Music is muted
        mutebutton.configure(image = unmute_button)
        pygame.mixer.music.set_volume(initial_volume)
        volume_scale.set(initial_volume * 100)
        statusbar['text'] = "Playing: "+ listofsongs[index]
        muted = False
    else:#Music is not muted
        initial_volume = volume
        mutebutton.configure(image = mute_button)
        pygame.mixer.music.set_volume(0)
        volume_scale.set(0)
        statusbar['text'] = "Muted "
        muted = True







drop_menu = Menu(root)
root.config(menu = drop_menu)


file_menu = Menu(drop_menu, tearoff = 0)
drop_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Open", command = directorychooser)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = root.quit)

help_menu = Menu(drop_menu, tearoff = 0)
drop_menu.add_cascade(label = "Help", menu = help_menu)
help_menu.add_command(label = "About Us", command = about_us)



root.title("Music PLayer")
#Status Bar
statusbar = Label(root, text = "Waiting for directory to be choosen", bd=1, relief = SUNKEN, anchor = W)# bd = border, sunken makes status bar deep, anchor= W meaning text will always appear in left
statusbar.pack(side = BOTTOM, fill = X)

#CONTROL
control_frame = Frame(root)
control_frame.pack(side = BOTTOM, fill = X)

previous_button=PhotoImage(file="images/previous-button.png")
previousbutton = Button(control_frame,image = previous_button, anchor = W)
previousbutton.pack(side = LEFT)

play_button=PhotoImage(file="images/play-button.png")
playbutton = Button(control_frame,image = play_button)
playbutton.pack(side = LEFT)

pause_button = PhotoImage(file="images/pause-button.png")
pausebutton = Button(control_frame, image = pause_button)
pausebutton.pack(side = LEFT)
  
stop_button = PhotoImage(file="images/stop-button.png")
stopbutton = Button(control_frame,image = stop_button)
stopbutton.pack(side = LEFT)

next_button = PhotoImage(file="images/next-button.png")
nextbutton = Button(control_frame,image = next_button)
nextbutton.pack(side = LEFT)

volume_scale = Scale(control_frame, from_ = 0, to = 100, orient = HORIZONTAL, command =set_vol)
volume_scale.set(80)
pygame.mixer.music.set_volume(0.8)
volume_scale.pack(side = RIGHT)

mute_button = PhotoImage(file="images/mute-button.png")
unmute_button = PhotoImage(file="images/unmute-button.png")
mutebutton = Button(control_frame,image = unmute_button)
mutebutton.pack(side = RIGHT, padx = 3, anchor = S)



previousbutton.bind("<Button-1>",prevsong)
playbutton.bind("<Button-1>",playsong)
pausebutton.bind("<Button-1>",pausesong)
stopbutton.bind("<Button-1>",stopsong)
nextbutton.bind("<Button-1>",nextsong)
mutebutton.bind("<Button-1>",mute_music)

#LABEL
label_frame = Frame(root)
label_frame.pack(side = BOTTOM, fill = X)

v = StringVar()
songlabel = Label(label_frame,textvariable=v, height = 2)
songlabel.pack(side = LEFT)

#LIST
list_frame = Frame(root)
list_frame.pack(side = RIGHT, fill = Y)
listbox = Listbox(list_frame, width = 30)
listbox.pack(fill = BOTH, expand = 1)



# MEDIA
media_frame = Frame(root)
media_frame.pack(side = LEFT, fill = BOTH, expand = YES)

displaybox = Listbox(media_frame)
displaybox.pack( expand = YES, fill = BOTH)









root.mainloop()