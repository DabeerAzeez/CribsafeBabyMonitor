'''
README:
If you run this file directly, a 'proof of concept' GUI will pop up (not connected to a sensor, so can be used for demonstration purposes
if the Pi is not available).
'''

import tkinter as tk
from tkinter.font import Font
from time import sleep
import random
import threading

WIDTH = 850
HEIGHT = 500

root = tk.Tk() # Initialize main window
root.title("CribSafe GUI")

def GUI_loop_random():
    """Updates GUI with random values every second"""
    
    while True: 
        on_off_var["text"] = str(bool(random.getrandbits(1)))
        facingup_var["text"] = str(bool(random.getrandbits(1)))
        standingup_var["text"] = str(bool(random.getrandbits(1)))
        is_fallen_var["text"] = str(bool(random.getrandbits(1)))

        alarm_var["text"] = random.choice(["High", "Low", "Off"])
        avg_accel["text"] = "(" + ",".join([str(random.randint(-3,3)) for i in range(3)]) + ")"
        avg_euler["text"] = "(" + ",".join([str(random.randint(50,150)) for i in range(3)]) + ")"

        sleep(1)
        
        root.update()



### Formatting ###

colors = {'red': '#FF2221',
          'green': '#20D613',
          'navy blue': '#084C61',
          'blue': '#177E89',
          'yellow': '#FFC857'}

title_font = Font(family='Helvetica', weight="bold", size=20)
header_1 = Font(family='Helvetica', weight="bold", size=16)
body_header = Font(family='Helvetica', size=14, underline=1)
body_font = Font(family='Helvetica', size=14)




### Canvas and Frames ###

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT) # Default window size, blank canvas
canvas.pack()

leftheadframe = tk.Frame(root, bg=colors['yellow']) # 'Frames' are what form the rectangular 'sections' of the GUI
leftheadframe.place(relwidth=0.25, relheight=0.2)

leftbodyframe = tk.Frame(root, bg=colors['yellow'])
leftbodyframe.place(relwidth=0.25, relheight=0.8, rely=0.2)

titleframe = tk.Frame(root, bg=colors['navy blue'])
titleframe.place(relwidth=0.75, relheight=0.2, relx=0.25)

mainframe = tk.Frame(root, bg=colors['blue'])
mainframe.place(relwidth=0.75, relheight=0.8, relx=0.25, rely=0.2)



### Labels ###  Make

# Title text

title = tk.Label(titleframe, text='CribSafe Child Monitor', font=title_font,
                 bg=colors['navy blue'], fg='white')
title.pack(side='left', expand=True)

# Main text

on_off = tk.Label(mainframe, text='On/Off: ', font=body_header, bg=colors['blue'], fg='white')
on_off.grid(row=0, column=0, padx=30, pady=30)

on_off_var = tk.Label(mainframe, text=1, font=body_font, bg=colors['blue'], fg='white')
on_off_var.grid(row=0, column=1, pady=30)

facingup = tk.Label(mainframe, text='Facing Up? ', font=body_header, bg=colors['blue'], fg='white')
facingup.grid(row=3, column=0, padx=30, pady=30)

facingup_var = tk.Label(mainframe, text='<facingup>', font=body_font, bg=colors['blue'], fg='white')
facingup_var.grid(row=3, column=1, pady=30)

standingup = tk.Label(mainframe, text='Standing Up? ', font=body_header, bg=colors['blue'], fg='white')
standingup.grid(row=1, column=0, padx=30, pady=30)

standingup_var = tk.Label(mainframe, text='<standingup>', font=body_font, bg=colors['blue'], fg='white')
standingup_var.grid(row=1, column=1, pady=30)

is_fallen = tk.Label(mainframe, text='Fallen Down? ', font=body_header, bg=colors['blue'], fg='white')
is_fallen.grid(row=2, column=0, padx=30, pady=30)

is_fallen_var = tk.Label(mainframe, text='<isfallen>', font=body_font, bg=colors['blue'], fg='white')
is_fallen_var.grid(row=2, column=1, pady=30)

alarm = tk.Label(mainframe, text='Alarm:'.center(16), font=body_header, bg=colors['blue'], fg='white')
alarm.grid(row=0, column=2, padx=30, pady=30)

alarm_var = tk.Label(mainframe, text='<alarm>', font=body_font, bg=colors['blue'], fg='white')
alarm_var.grid(row=0, column=3, padx=10, pady=30)

sensoraccel = tk.Label(mainframe, text='SensorAccel: ', font=body_header, bg=colors['blue'], fg='white')
sensoraccel.grid(row=1, column=2, padx=30, pady=30)

avg_accel = tk.Label(mainframe, text='<avgaccel>', font=body_font, bg=colors['blue'], fg='white')   #Display multiple lines of data using text widget?
avg_accel.grid(row=1, column=3, padx=10, pady=30)

sensoreuler = tk.Label(mainframe, text='SensorEuler: ', font=body_header, bg=colors['blue'], fg='white')
sensoreuler.grid(row=2, column=2, padx=30, pady=30)

avg_euler = tk.Label(mainframe, text='<avgeuler>', font=body_font, bg=colors['blue'], fg='white')
avg_euler.grid(row=2, column=3, padx=10, pady=30)

# Sidebar text

option_header = tk.Label(leftheadframe, text='Options', font=header_1, bg=colors['yellow'], fg='white')
option_header.pack(expand=True)




### Images ###

temp_logo = tk.PhotoImage(file="newcribsafe.png")
logo = temp_logo.subsample(5,5) # Downsize the original image
logolabel = tk.Label(titleframe, image=logo)
logolabel.pack(side='left')



### Checkboxes ###

dev_var = tk.IntVar()
dev = tk.Checkbutton(leftbodyframe, text='Developer Mode', variable=dev_var)
dev.grid(row=0, padx=30, pady=30)



if __name__ == '__main__': # Run the random GUI update function if this file is run directly
    update_GUI = threading.Thread(target=GUI_loop_random)
    update_GUI.start()

    root.mainloop()

# Code down here won't run (the main loop has been started)
