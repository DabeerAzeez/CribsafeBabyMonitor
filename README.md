# Cribsafe Baby Monitor

*Code written by: Dabeer Abdul-Azeez (abdulazd@mcmaster.ca) and Trevor Tung (tungt1@mcmaster.ca)*

## Overview
These python files compose the computational prototype for the *Cribsafe Baby Orientation Monitor* which will monitor a child's position and acceleration while they sleep, raising an alarm if the child is moving around too much in their sleep (e.g. if they fall out of their crib). This leaves the parents free to do what they want instead of having to constantly check in on the baby through more traditional auditory or visual baby monitors which don't usually have alarm systems to warn the parents if something has gone awry.

### Want more information?
1. See [here](https://dabeerazeez.wixsite.com/1p10portfolio/dp-3) to visit my website for more details on the project.
2. See [here](https://dabeerazeez.wixsite.com/1p10portfolio/dp-3-final-deliverables) for the final deliverables of the project, including videos, CAD files, the written proposal

If you want to recreate this yourself, see the final deliverables above for the 'Written Proposal', which includes more information on the design process, materials, circuitry, and CAD design for the housing of the device.

### Disclaimer
These files are meant to be run on a Raspberry Pi that is connected to an [Adafruit BNO055 Absolute Orientation Sensor](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black) and a buzzer. You won't be able to run them yourselves successfully unless you follow the circuit diagram included in the written proposal (see ['Want more information?'](#Want-more-information?) above).

**However**, you *can* run the `GUI.py` file without any other techonology (so long as you have Python 3.7 installed, newer versions cannot be guaranteed to work, but they probably will to my knowledge).

## Technologies Used
- These Python files were written for Python 3.7
- The GUI was created using the [Tkinter](https://docs.python.org/3/library/tkinter.html) library
- Multithreading was accomplished using the [threading](https://docs.python.org/3/library/threading.html) library
- [Raspberry Pi 3B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/), some LEDs, wires, a breadboard
- [Adafruit BNO055 Absolute Orientation Sensor](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black)
- A `sensor_library.py` file created by our course instructors for the 1P10 iBioMed Design Course at McMaster University

## Key Features
- Interfaces with an orientation sensor, a buzzer, and GUI using separate processing threads for increased responsiveness of the program to changes in the environment (see Multithreading in ['Technologies Used'](#Technologies-Used) above)
- Determines if the orientation sensor has fallen too quickly or turned over too far and activates various levels of buzzer alarms as necessary
- Outputs live sensor data and alarm status to a GUI