#MUSICS PLAYER
#source virt/Scripts/activate
#python player.py
from tkinter import*
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")
 
#Initialize Pygame

pygame.mixer.init()


#Create Function To Deal With Time

def play_time():
	#Check To See If Song Is Stopped
	if stopped:
		return
	#Grab Current Song Time
	current_time=pygame.mixer.music.get_pos() /1000
	#Convert Song Time To Time Format
	converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))
	
	song = playlist_box.get(ACTIVE)
	#song=f'D:/mp3/audio/{song}.mp3'
	#Find Current Song Length 
	song_mut=MP3(song)
	global song_length
	song_length=song_mut.info.length
	#Convert To Time Format
	converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))
	
	#Check To See If Song Is Over
	if int(song_slider.get()) == int(song_length):
		stop()
	elif paused:
		#Check To See If Paused If So -Pass
		pass
	else:
		#Move Slider Along 1 Second At A Time
		next_time =int(song_slider.get())+1
		#Output New Time Value To Slider
		song_slider.config(to=song_length,value=next_time)
		#Convert Slider Position To Time Formate
		converted_current_time=time.strftime('%M:%S',time.gmtime(int(song_slider.get())))
		#Output Slider
		status_bar.config(text=f'Time Elapsed :{converted_current_time} of {converted_song_length}  ')


	#Add Current Time To Status Bar 
	if current_time > 0:
		status_bar.config(text=f'Time Elapsed :{converted_current_time} of {converted_song_length}  ')
	#Create Loop To Check Time Every Second
	status_bar.after(1000,play_time)


#Create Function To Add One Song To Playlist

def add_song():
	song = filedialog.askopenfilename(initialdir='audio/' ,title="Choose A Song" ,filetypes=(("mp3 Files", "*.mp3"), ))
	#Strip Out Directory Structure And .mp3 From Song Title
	#song = song.relpace("D:/mp3/audio/", "")
	#song = song.replace(".mp3", "")
	#Add To Playlist
	playlist_box.insert(END, song) 


#Create Function To Add Many Songs To Playlist

def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/' ,title="Choose A Song" ,filetypes=(("mp3 Files", "*.mp3"), ))
	#Loop Through Song List And Replace Directory
	for song in songs:
		#Strip Out Directory Structure And .mp3 From Song Title
		#song = song.relpace("D:/mp3/audio/", "")
		#song = song.replace(".mp3", "")
		#Add To Playlist
		playlist_box.insert(END, song)


#Create Function To Delete One Song From Playlist

def delete_song():
	#Delete Highlighted Song From Playlist
	playlist_box.delete(ANCHOR)


#Create Function To Delete All Song From Playlist

def delete_all_songs():
	#Delete All Songs
	playlist_box.delete(0,END)


#Create Play Function

def play():
	#Set Stopped To False Since Song Is Playing
	global stopped
	stopped=False
	song = playlist_box.get(ACTIVE)
	#song=f'D:/mp3/audio/{song}.mp3'

	#Load Song With pygame Mixer
	pygame.mixer.music.load(song)
	#Play Song With pygame Mixer
	pygame.mixer.music.play(loops=0)

	#Get Song Time
	play_time()

#Create Stopped Variable
global stopped
stopped=False


#Create Stop Function
def stop():
	#Stop The Song
	pygame.mixer.music.stop()
	#Clear Playlist Bar
	playlist_box.selection_clear(ACTIVE)
	status_bar.config(text='')
	#Set Our Slider To Zero
	song_slider.config(value=0)
	#Set Stop Variable To True
	global stopped
	stopped=True

#Create Paused Variable
global paused
paused = False


#Create Pause Function
def pause(is_paused):
	global paused
	paused=is_paused
	if paused:
		#Pause
		pygame.mixer.music.unpause()
		paused=False
	else:
		#Pause
		pygame.mixer.music.pause()
		paused=True


#Create Function To Play The Next Song
def next_song():
	#Reset Sider Position And Status Bar
	status_bar.config(text='')
	song_slider.config(value=0)
	#Get Current Song Number
	next_one=playlist_box.curselection()
	#Add One To The Current Song no.tuple/list
	next_one=next_one[0]+1
	#Grab The Song Title From The Playlist
	song=playlist_box.get(next_one)
	#Load Song With pygame Mixer
	pygame.mixer.music.load(song)
	#Play Song With pygame Mixer
	pygame.mixer.music.play(loops=0)
	#Clear Active Bar In Playlist
	playlist_box.selection_clear(0,END)
	#More Active Bar To Next Song
	playlist_box.activate(next_one)
	#Set Active Bar To Next Song
	playlist_box.selection_set(next_one,last=None)


#Create Function To Play The Previous Song
def previous_song():
	#Reset Slider Position And Status Bar
	status_bar.config(text='')
	song_slider.config(value=0)
	#Get Current Song Number
	next_one=playlist_box.curselection()
	#Add One To The Current Song no.tuple/list
	next_one=next_one[0]-1
	#Grab The Song Title From The Playlist
	song=playlist_box.get(next_one)
	#Load Song With pygame Mixer
	pygame.mixer.music.load(song)
	#Play Song With pygame Mixer
	pygame.mixer.music.play(loops=0)
	#Clear Active Bar In Playlist
	playlist_box.selection_clear(0,END)
	#More Active Bar To Next Song
	playlist_box.activate(next_one)
	#Set Active Bar To Next Song
	playlist_box.selection_set(next_one,last=None)

#Create Volume Function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())


#Create Song Slider 
def slide(x):
	song = playlist_box.get(ACTIVE)
	#song=f'D:/mp3/audio/{song}.mp3'

	#Load Song With pygame Mixer
	pygame.mixer.music.load(song)
	#Play Song With pygame Mixer
	pygame.mixer.music.play(loops=0 ,start=song_slider.get())

#Create Main Frame
main_frame=Frame(root)
main_frame.pack(pady=20)

#Create Playlist Box
playlist_box = Listbox(main_frame, bg = "black", fg = "red", width = 60, selectbackground = "green", selectforeground = "black")
playlist_box.grid(row=0, column=0)

#Create Volume Slider Frame
volume_frame= LabelFrame(main_frame,text="Volume")
volume_frame.grid(row=0,column=1,pady=10)

#Create Volume Slider
volume_slider=ttk.Scale(volume_frame ,from_=0,to=1,orient=VERTICAL, length=125,value=1,command=volume)
volume_slider.pack(pady=10)

#Create Song Slider
song_slider=ttk.Scale(main_frame ,from_=0,to=100,orient=HORIZONTAL, length=360,value=0,command=slide)
song_slider.grid(row=2,column=0,pady=20)

#Define Button Images For Controls
back_btn_img = PhotoImage(file = 'image/back.png')
forward_btn_img = PhotoImage(file = 'image/forward.png')
play_btn_img = PhotoImage(file = 'image/play.png')
pause_btn_img = PhotoImage(file = 'image/pause.png')
stop_btn_img = PhotoImage(file = 'image/stop.png')

#Create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1,column=0,pady = 20)

#Create Play/Stop etc Buttons
back_button = Button(control_frame, image = back_btn_img, borderwidth = 0, command=previous_song)
forward_button = Button(control_frame, image = forward_btn_img, borderwidth = 0, command=next_song)
play_button = Button(control_frame, image = play_btn_img, borderwidth = 0, command=play)
pause_button = Button(control_frame, image = pause_btn_img, borderwidth = 0,command=lambda: pause(paused))
stop_button = Button(control_frame, image = stop_btn_img, borderwidth = 0, command=stop)

back_button.grid(row = 0, column = 0, pady = 10)
forward_button.grid(row = 0, column = 1, pady = 10)
play_button.grid(row = 0, column = 2, pady = 10)
pause_button.grid(row = 0, column = 3, pady = 10)
stop_button.grid(row = 0, column = 4, pady = 10)

#Create Menu
my_menu = Menu(root)
root.config(menu = my_menu)

#Create Add Song Menu Dropdown
add_song_menu = Menu(my_menu,tearoff = 0)
my_menu.add_cascade(label = "Add Songs", menu = add_song_menu)

#Add One Song to playlist
add_song_menu.add_command(label = "Add One Song To Playlist" , command = add_song)

#Add Many Songs to Playlist
add_song_menu.add_command(label = "Add Many Songs To Playlist" , command = add_many_songs)

#Create Delete Song Menu Dropddown
remove_song_menu = Menu(my_menu, tearoff = 0)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

#Create Status Bar
status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

#Temporary Label
my_label = Label(root,text = '')
my_label.pack(pady = 20)

root.mainloop()