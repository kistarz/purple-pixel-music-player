import tkinter as tk
import fnmatch
import os
from pygame import mixer
from mutagen.easyid3 import EasyID3

canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("430x500")
canvas.config(bg = "#FEF4FF")

rootpath = "Insert Your Music Folder Path Here"
pattern = "*.mp3"

mixer.init()

prev_img = tk.PhotoImage(file = "prev.png").subsample(8, 8)
stop_img = tk.PhotoImage(file = "stop.png").subsample(8, 8)
play_img = tk.PhotoImage(file = "play.png").subsample(8, 8)
pause_img = tk.PhotoImage(file = "pause.png").subsample(8, 8)
next_img = tk.PhotoImage(file = "next.png").subsample(8, 8)

is_paused = False
song_files = []

def play_song():
    global is_paused

    if is_paused:
        mixer.music.unpause()
        is_paused = False
    else:
        if not listbox.curselection():
            return
        file_index = listbox.curselection()[0]
        label.config(text=listbox.get(file_index))
        mixer.music.load(song_files[file_index])
        mixer.music.play()

def stop():
    mixer.music.stop()
    listbox.select_clear('active')

def play_next():
    if not listbox.curselection():
        return
    next_index = listbox.curselection()[0] + 1

    if next_index >= listbox.size():
        next_index = 0

    label.config(text=listbox.get(next_index))
    mixer.music.load(song_files[next_index])
    mixer.music.play()

    listbox.select_clear(0, 'end')
    listbox.activate(next_index)
    listbox.select_set(next_index)

def play_prev():
    if not listbox.curselection():
        return
    prev_index = listbox.curselection()[0] - 1

    if prev_index < 0:
        prev_index = listbox.size() - 1

    label.config(text=listbox.get(prev_index))
    mixer.music.load(song_files[prev_index])
    mixer.music.play()

    listbox.select_clear(0, 'end')
    listbox.activate(prev_index)
    listbox.select_set(prev_index)

def pause_song():
    global is_paused
    if not is_paused:
        mixer.music.pause()
        pauseButton["text"] = "Play"
        is_paused = True
    else:
        mixer.music.unpause()
        pauseButton["text"] = "Pause"
        is_paused = False

listbox = tk.Listbox(canvas, fg = "purple", bg = "#E0D5E6", width = 100, font = ('PixelPurl', 21), selectbackground="#F5F4F0", selectforeground="purple")
listbox.pack(padx = 15, pady = 20)

label = tk.Label(canvas, text = '', bg = '#FEF4FF', fg = 'purple', font = ('PixelPurl', 23))
label.pack(pady = 20)

top = tk.Frame(canvas, bg = "#FEF4FF")
top.pack(padx = 10, pady = 5, anchor = 'center')

prevButton = tk.Button(canvas, text = "Prev", image = prev_img, bg = '#FEF4FF', borderwidth = 0, command = play_prev)
prevButton.pack(pady = 20, in_ = top, side = 'left')

stopButton = tk.Button(canvas, text = "Stop", image = stop_img, bg = '#FEF4FF', borderwidth = 0, command = stop)
stopButton.pack(pady = 20, in_ = top, side = 'left')

playButton = tk.Button(canvas, text = "Play", image = play_img, bg = '#FEF4FF', borderwidth = 0, command = play_song)
playButton.pack(pady = 20, in_ = top, side = 'left')

pauseButton = tk.Button(canvas, text = "Pause", image = pause_img, bg = '#FEF4FF', borderwidth = 0, command = pause_song)
pauseButton.pack(pady = 20, in_ = top, side = 'left')

nextButton = tk.Button(canvas, text = "Next", image = next_img, bg = '#FEF4FF', borderwidth = 0, command = play_next)
nextButton.pack(pady = 20, in_ = top, side = 'left')

for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        filepath = os.path.join(root, filename)
        try:
            audio = EasyID3(filepath)
            title = audio.get('title', [os.path.splitext(filename)[0]])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
            display_name = f"{title} - {artist}"
        except Exception:
            display_name = os.path.splitext(filename)[0]
        listbox.insert('end', display_name)
        song_files.append(filepath)

canvas.mainloop()
