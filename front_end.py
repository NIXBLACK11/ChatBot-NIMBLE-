import json
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import speech
import chat2
import threading


global count
global message

message = ""
count = 1
win = Tk()
win.geometry("700x500")
BG_GRAY = "#ABB2B9"
BG_COLOR = "#010849"
TEXT_COLOR = "#FFFFFF"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# main
bgimg= tk.PhotoImage(file = "pa.png")
main_frame = Frame(win)
main_frame.pack(fill=BOTH, expand=1)


# canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
my_canvas.create_image( 0, 0, image = bgimg,anchor = "nw")

# scrollbar
my_scrollbar = tk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
#my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


#threading for speech functoin



def send(event, e):
    global message
    send = e.get()
    addLable(send)
        
    user = e.get().lower()
    message = chat2.chat2_o(user)
    if message == "weak":
        win.quit()
    addLable(message)

    e.delete(0, END)
    x = threading.Thread(target=speech.say, args=(message,))
    x.start()	


e = Entry(win, bg="#23272A", fg=TEXT_COLOR, font=FONT, width=70)
e.pack(anchor='e')
e.bind('<Return>', lambda eff: send(eff, e))


def addLable(message):
    # Creating and displaying a LabelFrame
    global count
    message = " "+message+" "
    if count%2==0:
        label = Label(my_canvas, text=message, bg="#282A2E", fg="white")
        label.pack()
        my_canvas.create_window(80, count*40, window=label, anchor='w')
    else:
        label = Label(my_canvas, text=message, bg="#199F36", fg="white")
        label.pack()
        my_canvas.create_window(530, count*40, window=label, anchor='w')
    
    if count > 10:
        my_canvas.yview_scroll(1, "units")
        
    count = count + 1

e.focus_set()
win.mainloop()