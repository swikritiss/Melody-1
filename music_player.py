import os
import time
from tkinter.filedialog import askdirectory

from mutagen.mp3 import MP3
import threading 

import pygame
from tkinter import *
import tkinter.messagebox

listofsongs = []
index = 0
count = 0
volume = 0.8
muted = False
song_changed = False

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
    displaybox.delete(0, END) 
    displaybox.insert(0, listofsongs[index])

def updatelabel():
    global index
    global songname
    root.title("Music Player: "+ listofsongs[index])

def update_details():
    audio = MP3(listofsongs[index])
    total_length = audio.info.length
    mins = int(total_length / 60)
    sec = round(total_length % 60)
    thread_1 = threading.Thread(target = start_count, args = (total_length,))   
    thread_1.start()

def start_count(total_length):
    global paused
    current_time = 0
    total_min = int(total_length / 60)
    total_sec = round(total_length % 60)
    total_time = (total_min * 60) + total_sec
    visual_detail["to"] = total_time
    pointer = index
    while current_time < total_time and pygame.mixer.music.get_busy():
        if pointer != index:
            return
        if paused:
            continue
        else:
            time.sleep(1)
            current_time = current_time + 1
            current_mins = int(current_time / 60)
            current_sec = round(current_time % 60)
            time_detail["text"] = "{:02d} : {:02d} / {:02d} : {:02d}".format(current_mins, current_sec, total_min, total_sec)
            visual_detail.set(current_time)
    if current_time == total_time:
        nextsong("<Button-1>")

def prevsong(event):
    global paused
    try:
        global index
        if index == 0:
            index = (count - 1)
        else:
            index -= 1
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        statusbar['text'] = "Playing: " + listofsongs[index]
        paused = False
        update_details()
        update_display()
    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')

def playsong(event):
    global index
    global paused
    global muted
    try:
        selected_song = listbox.curselection()
        if selected_song:
            index = int(selected_song[0])
            listbox.selection_clear(0, END)
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        statusbar['text'] = "Playing: "+ listofsongs[index] 
        paused = False
        muted = False
        update_details()
        update_display()
    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')

def pausesong(event):
    global index
    global paused
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
    global pause
    try:
        global index
        index = (index + 1) % count
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        statusbar['text'] = "Playing: "+ listofsongs[index]
        update_details()
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
detail_frame = Frame(root)
detail_frame.pack(side = BOTTOM, fill = X)

time_detail = Label(detail_frame, text = '--:-- / --:--')
time_detail.pack(side = RIGHT, anchor = S)

visual_detail = Scale(detail_frame, orient = HORIZONTAL, showvalue = 0)
visual_detail.pack(fill = X, expand = 1, side = LEFT)


v = StringVar()
'''
songlabel = Label(detail_frame,textvariable=v, height = 2)
songlabel.pack(side = LEFT)'''



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


'''def close_program():
    stopsong("<Button-1>")
    root.destroy()






root.protocol("WM_DELETE_WINDOW", close_program)'''
root.mainloop()