import math
import random
from time import sleep
import threading
from MyThread import *
from gpiozero import Button, TonalBuzzer

STAND_UP_TOL = 45   # Degrees from horizontal
FACING_UP_TOL = 45  # Degrees from horizontal
BUTTON_TIME = 3     # Number of seconds to hold button for toggle on/off
PWR_BUTTON_PIN = 7
AMPLITUDE_TOL = 9   # Magnitude of acceleration amplitude to trigger buzzer


power_button = Button(PWR_BUTTON_PIN)  # Power button initialized in this file because status function below requires it


def v_sum(vec):
    """Returns magnitude of inputted vector (with any number of dimensions)"""
    return math.sqrt(sum(i**2 for i in vec))


def vector_list_average(vector_list):
    """Returns averaged vector from a list of vectors (with any number of dimensions)"""
    return [round(sum(i)/len(i), 2) for i in zip(*vector_list)]

def amplitude(data_set):
    """Determines amplitude from a list of data"""
    return abs(max(data_set)-min(data_set))


def countingbooleans(boolean, boolcounter, tol, alarm_value):
    """Determines if enough outputs of a specific boolean have been received in order to warrant switching the buzzer boolean to its 'alarm value'
    (i.e. the value that would trigger an alarm, so 'TRUE' for 'Standing Up' but 'FALSE' for 'Facing Up'"""
    try:
        boolean_b = not alarm_value
    except TypeError:
        print("Tried inverting a non-boolean!")

    if boolean != alarm_value and boolcounter < tol: # Check for 'tol' number of 'boolean' triggers in order to update the buzzer boolean
        boolcounter = 0                              # which is linked to the buzzer thread and the GUI
    else:
        boolcounter += 1

    if boolcounter >= tol: # Once the buzzer boolean has been triggered, ensure that the alarm remains on until the parent switches off the device
        boolean = targetval
        boolean_b = targetval

    return boolean, boolcounter, boolean_b


def obj1_status(is_on):
    """(Status) Checks to see if user is trying to long-press the power button (i.e. trying to toggle device on/off)"""
    button_counter = 0

    while power_button.is_pressed:
        button_counter += 1
        sleep(1)

        if button_counter >= BUTTON_TIME:
            button_counter = 0
            is_on = not is_on # Flip 'on' status

            if is_on: # Display appropriate message for shutdown or startup, since this function is used for both purposes
                print("Beginning main process")
            else:
                print("Shutting down")

            return is_on

    return is_on


def obj2_baby_stand_up(avg_euler_z):
    """(Notification) Determines if baby is standing up (according to alignment of spine relative to horizontal)"""
    return False if STAND_UP_TOL < abs(avg_euler_z) - 90 else True
    # 90 degrees = standing straight up


def obj3_fall_detection(recent_accels):
    """(Escalation) Determines if baby has fallen (according to the magnitude of the amplitude of recent acceleration values)"""
    accel_magnitudes = [v_sum(i) for i in recent_accels]  # Determines magnitude of each acceleration vector in the recent accelerations list
    accel_amplitude = amplitude(accel_magnitudes)
    return True if accel_amplitude > AMPLITUDE_TOL else False  # Checks if amplitude of recent accelerations vectors is too high
                                                               # (indicating a fall / large acceleration)

def obj4_facing_up(avg_euler_y):
    """Determines if baby is face down"""
    return False if abs(avg_euler_y) > (90 - FACING_UP_TOL) else True
    # 90 degrees = rolled onto left side; -90 degrees = rolled onto right side
