import os
from tkinter.filedialog import askdirectory
from functions import *

import pygame
from tkinter import *

listofsongs = []
index = 0
status = ['play', 'pause']
status_index = 1


def directorychooser():
    directory = askdirectory()
    os.chdir(directory)
 
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            listofsongs.append(files)
    update_list()
 
 
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    update_list()

def update_list():
    listofsongs.reverse()
    for items in listofsongs:
        listbox.insert(0,items)     
    listofsongs.reverse()

def updatelabel():
    global index
    global songname
    root.title("Music Player: "+ listofsongs[index])
    v.set(listofsongs[index])
    
def prevsong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    print(index)
    updatelabel()

def playsong(event):
    global index
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def pausesong(event):
    global index
    global status_index
    pygame.mixer.music.load(listofsongs[index])
    if status_index == 1:
        pygame.mixer.music.pause()
        status_index = 0
    else:
        pygame.mixer.music.unpause()
        status_index = 1
    print(status_index)


def nextsong(event):
    global index
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    print(index)
    updatelabel()


 
 
def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")