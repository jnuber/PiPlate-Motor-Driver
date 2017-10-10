#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  PiPlateMotor_Driver.py
#  
#  Copyright 2017 John Nuber <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
import time
from time import sleep
import pygame
import piplates.MOTORplate as MOTOR          #import the MOTORplate module

# Define Motors
FL = 1				# Define Motor 1 = Front Left - FL
FR = 2  			# Define Motor 2 = Fright Right - FR
RL = 3  			# Defome Motor 3 = Rear Left - RL
RR = 4  			# Define Motor 4 = Rear Right - RR

# Define inital motor parameters
direction = "Stopped" # Forward / Backwards / Left / Right
status    = "Stopped"    # Stopped / running / 
speed = 0			# Initalize motor speed 0 - 100
rate  = 0.0			# Initalize aceleration rate 0 - 100

# Function to set all drives off
def MotorOff():
    print("Stopping Motor")
    motor.dcSTOP(ctl,1)
    motor.dcSTOP(ctl,2)
    motor.dcSTOP(ctl,3)
    motor.dcSTOP(ctl,4)
    
    status = "stopped"

def resetCtl():
	MOTOR.clrLED(ctl)
	sleep(2)
	MOTOR.RESET(ctl)
	return

def initMotor(rotation):
	print("Setting: ",rotation)
	motor.dcCONFIG(ctl,1,rotation,0.0,0.0)
	motor.dcCONFIG(ctl,2,rotation,0.0,0.0)
	motor.dcCONFIG(ctl,3,"cw",0.0,0.0)
	motor.dcCONFIG(ctl,4,"cw",0.0,0.0)
	
	motor.dcSTART(ctl,1)
	motor.dcSTART(ctl,2)
	motor.dcSTART(ctl,3)
	motor.dcSTART(ctl,4)
	
	status = "running"
	return

def fwd():
	print("Forward motion called. CTL: ",ctl)
	motor.dcCONFIG(ctl,1,"cw",50,100.0)
	motor.dcCONFIG(ctl,2,"cw",50,100.0)
	motor.dcCONFIG(ctl,3,"cw",50,100.0)
	motor.dcCONFIG(ctl,4,"cw",50,100.0)
	
	motor.dcSTART(ctl,1)
	motor.dcSTART(ctl,2)
	motor.dcSTART(ctl,3)
	motor.dcSTART(ctl,4)

def speed(FLspeed,FRspeed,RLspeed,RRspeed):
	print("Adjusting Speed {0}: {1} ".format(FL,FLspeed))
	print("Adjusting Speed {0}: {1} ".format(FR,FRspeed))
	print("Adjusting Speed {0}: {1} ".format(RL,RLspeed))
	print("Adjusting Speed {0}: {1} ".format(RR,RRspeed))	
	motor.dcSPEED(ctl,FR,FLspeed)
	motor.dcSPEED(ctl,FL,FRspeed)
	motor.dcSPEED(ctl,RR,FLspeed)
	motor.dcSPEED(ctl,RL,FRspeed)

# Settings for JoyStick
leftDrive  = FL                         # Drive number for left motor
rightDrive = FR                         # Drive number for right motor
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 0                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
global button12
global rotation 

hadEvent  = True
moveUp    = False
moveDown  = False
moveLeft  = False
moveRight = False
moveQuit  = False
button12  = False
rotation  = 'cw'

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("JoyBorg - Press [ESC] to quit")

motor = MOTOR
global ctl
ctl = 1

print("Reset and initalize controller {0} and motors".format(ctl))
resetCtl()

# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    global button12
    global upDown
    global leftRight
    
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = False
        elif event.type == pygame.JOYAXISMOTION:
            # A joystick has been moved, read axis positions (-1 to +1)
            hadEvent = True
            upDown    = float(joystick.get_axis(axisUpDown))
            leftRight = float(joystick.get_axis(axisLeftRight))
            button12  = joystick.get_button(12)
            # Invert any axes which are incorrect
            if axisUpDownInverted:
                upDown = -upDown
            if axisLeftRightInverted:
                leftRight = -leftRight
            # Determine Up / Down values
            if upDown < -0.1:
                moveUp   = True
                moveDown = False
            elif upDown > 0.1:
                moveUp   = False
                moveDown = True
            else:
                moveUp   = False
                moveDown = False
            # Determine Left / Right values
            if leftRight < -0.1:
                moveLeft  = True
                moveRight = False
            elif leftRight > 0.1:
                moveLeft  = False
                moveRight = True
            else:
                moveLeft  = False
                moveRight = False      
try:
    print('Press [ESC] to quit')
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            if moveQuit:
                break
            elif button12:
                print("Exiting Motor Drivers") 
                break   
            elif moveLeft:
                print("Left")
                if status == "stopped": 
                   initMotor('cw')
                if direction == "fwd":
                    speed((upDown * -100),(upDown * -50),(upDown * -100),(upDown * -50)) # FL, FR, RL,RR
                elif direction == "reverse":
                    speed((upDown * 100 ),(upDown * 50 ),(upDown * 100 ),(upDown * 50 )) # FL, FR, RL,RR
            elif moveRight:
                print("Right")
                if status == "stopped": 
                   initMotor('ccw')
                if direction == "fwd":
                    speed((upDown * -50),(upDown * -100),(upDown * -50),(upDown * -100)) # FL, FR, RL,RR
                elif direction == "reverse":
                    speed((upDown * 50 ),(upDown * 100 ),(upDown * 50 ),(upDown * 100 )) # FL, FR, RL,RR
            elif moveUp:
                if direction != "fwd":
                    MotorOff()
                    initMotor('cw')
                print("Fwd @ {0}".format(upDown * -100))
                speed((upDown * -100),(upDown * -100),(upDown * -100),(upDown * -100))
                direction = "fwd"
                status = "running"
            elif moveDown:
                if direction != "reverse":
                    MotorOff()
                    initMotor('ccw')
                print("Back @ {0}".format(upDown * 100))
                speed((upDown * 100),(upDown * 100),(upDown * 100),(upDown * 100))
                direction = "reverse"
                status = "running"
            else:
                # print("center")
                if direction != "stopped":
                    MotorOff()
                    direction = "stopped"
                    status = "stopped"
        time.sleep(interval)
    # Disable all drives
    MotorOff()
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    MotorOff()
