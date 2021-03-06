from tkinter import *
import tkinter
import time
from turtle import window_width
import rtmidi
from subprocess import Popen
import serial

window = tkinter.Tk() 
panedTest = tkinter.PanedWindow(window)
panedTest.pack(fill="both", expand=1)

p1 = tkinter.PanedWindow(panedTest)
p1.configure(bg="black")
p1.pack(fill="both", expand=1, side=tkinter.LEFT)
p2 = tkinter.PanedWindow(panedTest)
p2.configure(bg="black")
p2.pack(fill="both", expand=1, sid=tkinter.LEFT)
p3 = tkinter.PanedWindow(panedTest)
p3.configure(bg="black")
p3.pack(fill="both", expand=1, side=tkinter.LEFT)

def midiBall():
    # init Arduino on Port
    ser = serial.Serial('/dev/cu.usbmodem142101',9600)

    # init midiout library
    midiout = rtmidi.MidiOut()

    # get available ports from input device
    available_ports = midiout.get_ports()
    print(available_ports)

    # default values
    gyroY = None
    gyroZ = None
    isRotatedBooleanZLeft = False
    isRotatedBooleanZRight = False
    isRotatedBooleanYRight = False
    isRotatedBooleanYLeft = False
    isPressed = False
    aktPitch = 2
    editMode = False
    play = False
    rec = False
   
    # start program
    while True:

        # read signal from arduino
        command = ser.readline()
        
        if command:
            sig_value = int(command)
            value = int(ser.readline())
            
            # edit-button is pressed
            if sig_value == 0:

                if editMode:
                    editMode = False
                    print("exit Edit-Mode")
                    p3.configure(bg="black")
                    p3.update()
                else:
                    editMode = True
                    print("start Edit-Mode") 
                    p3.configure(bg="orange")
                    p3.update()

                        
                if available_ports:
                    midiout.open_port(0)

                    with midiout:
                        note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
                        note_off = [0x80, 60, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)

            
            # record-button is pressed
            elif sig_value == 1:
                
                if rec:
                    rec = False
                    print("stopped recording")
                    p2.configure(bg="black")
                    p2.update()
                else:
                    rec = True
                    print("start recording")
                    p2.configure(bg="red")
                    p2.update()

                if available_ports:
                    midiout.open_port(0)
                    
                    with midiout:
                        note_on = [0x90, 61, 112] # channel 1, middle C#, velocity 112
                        note_off = [0x80, 61, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)

            # play-button is pressed    
            elif sig_value == 2:

                if play:
                    play = False
                    print("stop")
                    p1.configure(bg="black")
                    p1.update()
                else:
                    play = True
                    print("play")
                    p1.configure(bg="green")
                    p1.update() 

                if available_ports:
                    midiout.open_port(0)

                    if play:
                        with midiout:
                            note_on = [0x90, 62, 112] # channel 1, middle D, velocity 112
                            note_off = [0x80, 62, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)
                    else:
                        with midiout:
                            note_on = [0x90, 63, 112] # channel 1, middle D, velocity 112
                            note_off = [0x80, 63, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)
        
            # rotate midiball to front or to back
            elif sig_value == 3:
                
                if gyroY is None: 
                    gyroY = value
                    continue
            
                if isRotatedBooleanYRight:
                    if value < (gyroY + 3500):
                        isRotatedBooleanYRight = False
                elif value > (gyroY + 7000):
                    isRotatedBooleanYRight = True

                    if available_ports:
                        midiout.open_port(0)

                    if editMode:
                        with midiout:
                            note_on = [0x90, 68, 112] # channel 1, middle G#, velocity 112
                            note_off = [0x80, 68, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)
                    else: 
                        with midiout:
                            note_on = [0x90, 66, 112] # channel 1, middle F#, velocity 112
                            note_off = [0x80, 66, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)

                    print("drehung rechts")
                    print(value)

                if isRotatedBooleanYLeft:
                    if value > (gyroY - 3500):
                            isRotatedBooleanYLeft = False
                elif value < (gyroY - 7000):
                    isRotatedBooleanYLeft = True

                    if available_ports:
                        midiout.open_port(0)

                    if editMode:
                        with midiout:
                            note_on = [0x90, 69, 112] # channel 1, middle A, velocity 0
                            note_off = [0x80, 69, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)
                    else:
                        with midiout:
                            note_on = [0x90, 65, 112] # channel 1, middle F, velocity 0
                            note_off = [0x80, 65, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)
                        
                    print("drehung Links")
                    print(value)
                    
            # rotate midiball left or right
            elif sig_value == 4:
                
                if gyroZ is None: 
                    gyroZ = value
                    continue
            
                if isRotatedBooleanZRight:
                    if value < (gyroZ + 3500):
                        isRotatedBooleanZRight = False
                elif value > (gyroZ + 9000):
                    isRotatedBooleanZRight = True

                    if available_ports:
                        midiout.open_port(0)

                    if editMode:
                        if aktPitch == 0: 
                            # von runtergepitcht auf halb runter hochpitchen 
                            minPitch = 52
                            maxPitch = 59
                        elif aktPitch == 1:
                            # von halbe runtergepitcht auf normal hoch pitchen
                            minPitch = 58
                            maxPitch = 65
                        elif aktPitch == 2:
                            # von normal auf halb hoch pitchen
                            minPitch = 63
                            maxPitch = 70
                        else:
                            # von halbe Oktave hoch auf ganze Oktave hoch pitchen
                            minPitch = 70
                            maxPitch = 76

                        with midiout:
                            for k in range(minPitch, maxPitch):
                                fader = [0xE0, 10, k]
                                midiout.send_message(fader)
                                midiout.send_message(fader)
                                time.sleep(0.01)
                        if aktPitch < 4:
                            aktPitch += 1

                    else: 
                        with midiout:
                            note_on = [0x91, 62, 112] # channel 1, middle B, velocity 112
                            note_off = [0x81, 62, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)

                    print("drehung rechts")
                    print(value)

                if isRotatedBooleanZLeft:
                    if value > (gyroZ - 3500):
                        isRotatedBooleanZLeft = False
                elif value < (gyroZ - 9000):
                    isRotatedBooleanZLeft = True

                    if available_ports:
                        midiout.open_port(0)

                    if editMode:
                        if aktPitch == 4:
                            # von hochgepitcht auf halb hoch runter pitchen
                            minPitch = 76
                            maxPitch = 68
                        elif aktPitch == 3:
                            # von halb hoch gepitcht auf normal runter pitchen
                            minPitch = 70
                            maxPitch = 63
                        elif aktPitch == 2:
                            # von normal halb runter pitchen
                            minPitch = 64
                            maxPitch = 58
                        else:
                            # von halb runter ganze Oktave runter pitchen
                            minPitch = 58
                            maxPitch = 52
                            
                        with midiout:
                            for k in range(minPitch, maxPitch, -1):
                                fader = [0xE0, 10, k]
                                midiout.send_message(fader)
                                midiout.send_message(fader)
                                time.sleep(0.01)
                        
                        if aktPitch > 0:
                            aktPitch -= 1

                    else:
                        with midiout:
                            note_on = [0x91, 60, 112] # channel 1, middle C, velocity 112
                            note_off = [0x81, 60, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)
                        
                    print("drehung Links")
                    print(value)

            # midiball is pressed    
            elif sig_value == 5:

                if isPressed:
                    if value < 190:
                        isPressed = False
                    
                elif value > 210: 
                    isPressed = True

                    if available_ports:
                        midiout.open_port(0)

                        with midiout:
                            note_on = [0x90, 67, 112] # channel 1, middle G, velocity 112
                            note_off = [0x80, 67, 0] 
                            midiout.send_message(note_on)
                            time.sleep(0.1)
                            midiout.send_message(note_off)
                    
            else:
                print("!!!didnt match!!!")


window.title('Midi Ball')
window.geometry("720x360+10+20")
window.after(100, midiBall)
window.mainloop()