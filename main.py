### DP3 TEAM 7 PYTHON PROGRAM ###
### Computing Subteam: Dabeer Abdul-Azeez (abdulazd) & Trevor Tung (tungt1)
### Date Submitted: February 14th, 2020

'''
DISCLAIMER:

This python program has multiple threads to allow for pieces of code to run concurrently:
    - One for the main loop
    - One for the GUI
    - And one for the buzzer output

The submitted folder includes multiple python files:
    - A main file (main loop, variables, multithread-functions)
    - An objectives file (all functions which are not targeted by their own thread, including all four objectives)
    - A MyThread file (a threading subclass definition, used in the main file to run the GUI and buzzer in parallel with the main while loop)
    - A GUI file (which initializes the GUI that is updated in the main file by its own thread)

    - There is also a logo image which is used by the GUI, feel free to open it up in full resolution and save it to your desktop
    - and some .idea / venv folders which were made by PyCharm... we didn't want to delete them just to be safe

A bug we've noticed...
    - Sometimes the 'fall detection' detects false positives when the device is still. We think this is due to sensor inaccuracies. 
      Please restart the program if you face such challenges.

'''


### SETUP ###
from gpiozero import Button, RGBLED, TonalBuzzer
from sensor_library import *
from objectives import * # Import some functions
from MyThread import * # Import a threading subclass

# Constants
LIST_LENGTH = 10  # Length of list of most recent data points recorded from sensor
REFRESH_RATE = 20 # Refresh rate of GUI and main loop (in Hertz)

STANDING_TOL = 10 # <-- These tolerances correlate to how long an environmental condition (i.e. facing down)
FALLING_TOL = 6   # must be recognized by the program for it to update the buzzer and actually trigger the alarm
FACING_TOL = 10

ROT_BUTTON_PIN = 21 # Pins for GPIO devices
BUZZER_PIN = 18
RGBPINS = (17, 27, 22)

# Variables and lists
is_on = False       # Boolean for whether the monitor is on or off
rotation_on = False # Boolean for whether the rotation alarm is on or off

facing_up = True    # Booleans which represent the baby's position
standing_up = False
is_fallen = False

facing_up_b = True    # Extra booleans to be used by the buzzer and GUI (triggered only if above 'normal' 
is_fallen_b = False   # booleans are triggered for long enough (to prevent erratic sensor data from turning
standing_up_b = False # on an alarm

counter_r = 0
counter_f = 0
counter_s = 0

recent_accels = []  # Initialize lists to keep recent readings
recent_eulers = []
recent_averaged_accels = []
avg_accel = ["No input detected"] # Initialize average values for the GUI
avg_euler = ["No input detected"]

# Initialize input/output devices, with 'off' as initial value as necessary
try:
    sensor = Orientation_Sensor()   
    rotation_button = Button(ROT_BUTTON_PIN)             # Power button (not seen here) initialized in objectives file as
    buzzer = TonalBuzzer(BUZZER_PIN, initial_value=None) # it is not needed in this file
    status = RGBLED(red=RGBPINS[0], green=RGBPINS[1], blue=RGBPINS[2], initial_value=(0,0,0))
except ValueError:
    print("Please check the wiring of your sensor / buzzer / LED / buttons!")
    print("This program will now exit")
    sleep(2)
    exit()


### FUNCTIONS TO BE RUN BY THREADS ###

def buzzer_choice():
    """Plays appropriate buzzer pattern depending on value of appropriate booleans"""

    tune = 0  # Initial value

    while True:
        tune = thread_buzz.val[0] # Read the tune value from the buzzer thread

        # Play appropriate tune based on 'tune' value (no tune played for tune value of 0)
        if tune == 1:  # Facing down -- Low alarm
            thread_buzz.val[1] = "LOW" # Set buzzer thread's 'alarm' value to "LOW"
            buzzer.play("C5")          # (for use in print statements / GUI)
            sleep(1)
            buzzer.stop()
            sleep(1)

        elif tune == 2:  # Standing Up -- Low alarm
            thread_buzz.val[1] = "LOW"
            buzzer.play("C5")
            sleep(1)
            buzzer.stop()
            sleep(1)

        elif tune == 3:  # Fallen down -- High alarm
            thread_buzz.val[1] = "HIGH"
            buzzer.play("A5")
            sleep(0.1)
            buzzer.play("A4")
            sleep(0.1)
            buzzer.play("A5")
            sleep(0.1)
            buzzer.play("A4")
            sleep(0.1)
            buzzer.stop()
            sleep(0.5)

        sleep(0.2)

def GUI_mainloop():
    from GUI import colors # Import colors dictionary from GUI file
    import GUI  # Imported GUI file inside GUI_mainloop (i.e. inside this 'thread') because of Tkinter's limited multithreading capabilities.
                # Specifically, "mainloop()" (called below) must be started inside the same thread where Tkinter is imported, 
                # meaning that 'import GUI' must be done within this GUI_mainloop() function because the GUI file itself imports Tkinter

    COL2WIDTH = 6 # Formatting for GUI columns
    COL4WIDTH = 14

    def GUI_update(): 
        """Updates GUI with new values at the end of each second"""
        # Defined this function inside GUI_mainloop so i) 'after' function below can call it and ii) so it can read/write to GUI labels
        # (imported one level above)
    
        while True: 
            GUI.on_off_var.config(text= "ON" if is_on else "OFF")

            if is_on: # Update GUI labels with appropriate text based on the values of relevant variables
                if rotation_on: 
                    GUI.facingup_var.config(text=("YES" if facing_up_b else "NO").center(COL2WIDTH),fg= colors['green'] if facing_up_b else colors['red'])
                else:
                    GUI.facingup_var.config(text="OFF", fg='white')
                GUI.standingup_var.config(text=("YES" if standing_up_b else "NO"), fg= colors['red'] if standing_up_b else colors['green'])
                GUI.is_fallen_var.config(text=("YES" if is_fallen_b else "NO"), fg= colors['red'] if is_fallen_b else colors['green'])
                GUI.alarm_var.config(text=thread_buzz.val[1].center(COL4WIDTH))
                
                if GUI.dev_var.get() == 1: # Hide or show acceleration / euler values based on whether 'Developer Options' checkbox is ticked
                    GUI.sensoraccel.config(text="SensorAccel:")
                    GUI.avg_accel.config(text=str(avg_accel))
                    GUI.sensoreuler.config(text="SensorAccel:")
                    GUI.avg_euler.config(text=str(avg_euler))

                else:
                    GUI.sensoraccel.config(text="")
                    GUI.avg_accel.config(text="")
                    GUI.sensoreuler.config(text="")
                    GUI.avg_euler.config(text="")

            else: # Show blank ---- lines if program is 'off' according to is_on boolean
                GUI.facingup_var.config(text="-----",fg='white')
                GUI.standingup_var.config(text="-----",fg='white')
                GUI.is_fallen_var.config(text="-----",fg='white')

                GUI.alarm_var.config(text="".center(COL4WIDTH, "-"),fg='white')

                if GUI.dev_var.get() == 1: 
                    GUI.sensoraccel.config(text="SensorAccel:")
                    GUI.avg_accel.config(text="".center(COL4WIDTH, "-"))
                    GUI.sensoreuler.config(text="SensorEuler:")
                    GUI.avg_euler.config(text="".center(COL4WIDTH, "-"))

                else: # Hide sensor accel / euler entries if 'Developer Options' checkbox is not ticked
                    GUI.sensoraccel.config(text="")
                    GUI.avg_accel.config(text="")
                    GUI.sensoreuler.config(text="")
                    GUI.avg_euler.config(text="")

            GUI.root.update()

            sleep(1/REFRESH_RATE)

    GUI.root.after(1000, GUI_update) # Runs GUI_update function 1000ms after this line of code is run, allowing
                                     # for i) mainloop() (below) to be initiated and ii) while True function (in GUI_update) to be run

    GUI.root.mainloop() # Starts main loop for GUI (gets the GUI running)

# Creating / Starting of Threads
thread_buzz = MyThread(buzzer_choice) # Initialize buzzer thread (running 'buzzer_choice' function)
thread_buzz.start()
thread_buzz.val = [0, "OFF"]  # thread_buzz.val = ['tune #', 'alarm level']

thread_GUI = threading.Thread(target=GUI_mainloop) # Initialize GUI thread (running 'GUI_mainloop' function)
thread_GUI.start()



### MAIN FUNCTION ###

def main():
    global is_on # Import global variables for modification within the main function
    global rotation_on
    global facing_up_b
    global standing_up_b
    global is_fallen_b
    global facing_up
    global standing_up
    global is_fallen
    global counter_r
    global counter_f
    global counter_s

    global recent_accels
    global recent_eulers
    global recent_averaged_accels
    global avg_accel
    global avg_euler

    print('''Welcome to the 'CribSafe' Baby Monitoring System! After placing your child
    to sleep, place the device in your child's clothing pocket with the arrow pointing up.

    With this device, you can:
    - Press and hold the power button for three seconds to turn the device on
    - Press and hold the power button for three seconds to turn the device off (once on)
    - Turn on/off the side-to-side rotation alarm (LED will turn blue when rotation alarm is on)
    - Monitor whether your child is standing up or lying down
    - Monitor whether your child has experienced a fall''')

    while True:

        try:

            while not is_on:
                button_counter = counter_f = counter_s = counter_r = 0  # Reset counters
                thread_buzz.val = [0, "OFF"] # Default values for buzzer thread
                status.off()

                is_on = obj1_status(is_on) # Check if user is trying to power on the device

            while is_on: # Main loop if device has been turned on

                if rotation_on: # Green colour for LED if rotation alarm is off, blue if on
                    status.color = (0, 0, 1)
                else:
                    status.color = (0, 1, 0)

                # Check if user is trying to turn toggle the baby rotation alarm
                if rotation_button.is_pressed:
                    rotation_on = not rotation_on
                    sleep(0.4)  # Have a short sleep to prevent 'rotation_on' from toggling back and forth too fast

                # Extract sensor information to variables for further calculations
                accel = sensor.accelerometer()  
                euler = sensor.euler_angles()   

                # List management (restrict data set to 10 most recent valid sensor inputs)
                if accel[0] is not None:  # Prevents 'None's being read from the sensor (Nones preclude proper avg. calculations)
                    recent_accels.append(accel)

                if euler[0] is not None:
                    euler = [abs(i) for i in euler] # Read absolute values of euler angles (negative values unnecessary 
                    recent_eulers.append(euler)     # for our program, and absolute values improve calculation accuracy)

                if len(recent_accels) > LIST_LENGTH: # Limits list length by deleting surplus entries from the beginning of the list
                    diff = len(recent_accels) - LIST_LENGTH
                    del recent_accels[0:diff]

                if len(recent_eulers) > LIST_LENGTH:
                    diff = len(recent_eulers) - LIST_LENGTH
                    del recent_eulers[0:diff]

                # Take average of the most recent readings
                avg_accel = vector_list_average(recent_accels)
                avg_euler = vector_list_average(recent_eulers)

                recent_averaged_accels.append(avg_accel) # List of recent averaged accelerations to be used for objective 3 (calculation 
                                                         # of amplitude needs multiple data points)

                if len(recent_averaged_accels) > LIST_LENGTH:
                    diff = len(recent_averaged_accels) - LIST_LENGTH
                    del recent_accels[0:diff]

                # Run through objectives
                try:
                    standing_up = obj2_baby_stand_up(avg_euler[2])
                    is_fallen = obj3_fall_detection(recent_averaged_accels) 
                    if rotation_on:
                        facing_up = obj4_facing_up(avg_euler[1])
                        
                except IndexError: # Index Error randomly occurred during testing, possibly due to sensor malfunction
                    print("Sensor index error...retaking data.")
                    
                # Check if standing_up / is_fallen / facing_up checks have been triggered for long enough to
                # warrant activating the buzzer and updating the GUI
                
                standing_up, counter_s, standing_up_b = countingbooleans(standing_up, counter_s, STANDING_TOL, True)
                is_fallen, counter_f, is_fallen_b = countingbooleans(is_fallen, counter_f, FALLING_TOL, True)
                facing_up, counter_r, facing_up_b = countingbooleans(facing_up, counter_r, FACING_TOL, False)

                # Determine appropriate tune to play from value of buzzer booleans and assigned hierarchy
                # (i.e. 'Fallen down' alarm is more important than the 'standing up' or 'facing down' alarms)
                if not facing_up_b:
                    tune = 1
                if standing_up_b:
                    tune = 2
                if is_fallen_b:
                    tune = 3
                if facing_up_b and not standing_up_b and not is_fallen_b:
                    tune = 0

                # Pass the buzzer thread the value of the tune that should be played
                thread_buzz.val[0] = tune

                # Print Statement
                print(f"On?: {is_on} | Rotation Alarm On?: {rotation_on} | Face Up?: {facing_up} | Standing Up?: {standing_up} | Fallen?: {is_fallen} | BUZZER: {thread_buzz.val[1]}")
                
                is_on = obj1_status(is_on)  # Check if user is trying to turn off the device

                sleep(1/REFRESH_RATE)  # Sleep for a bit so as not to overwork the system.

        except OSError or ValueError:

            print("Please check your wiring again and restart the program!")

main()
