
import time
import rtmidi
from subprocess import Popen
import serial

ser = serial.Serial('/dev/cu.usbmodem142101',9600)
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)
gyroY = None
gyroZ = None
isRotatedBooleanZLeft = False
isRotatedBooleanZRight = False
isRotatedBooleanYRight = False
isRotatedBooleanYLeft = False
isPressed = False
minPitch = 0
maxPitch = 0
editMode = False
while True:
    command = ser.readline()
    
    if command:
        sig_value = int(command)
        value = int(ser.readline())
        
        if sig_value == 0:
            
            print("Button 1 klick")
            print("buttonValue: " + str(value))

            if editMode:
                editMode = False
            else:
                editMode = True 
                    
            if available_ports:
                midiout.open_port(0)

                with midiout:
                    note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
                    note_off = [0x80, 60, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            
        elif sig_value == 1:

            print("Button 2 klick")
            print("buttonValue: " + str(value))

            if available_ports:
                midiout.open_port(0)
                 
                with midiout:
                    note_on = [0x90, 61, 112] # channel 1, middle D, velocity 112
                    note_off = [0x80, 61, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.1)
                    midiout.send_message(note_off)

            
        elif sig_value == 2:

            print("Button 3 klick")
            print("buttonValue: " + str(value))

            if available_ports:
                midiout.open_port(0)

                with midiout:
                    note_on = [0x90, 62, 112] # channel 1, middle E, velocity 112
                    note_off = [0x80, 62, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.1)
                    midiout.send_message(note_off)
                         
        elif sig_value == 3:
        
            if value > 10000:
                print("push")
                if available_ports:
                    midiout.open_port(0)
                    with midiout:
                        note_on = [0x90, 63, 112] # channel 1, middle F, velocity 112
                        note_off = [0x80, 63, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.5)
                        midiout.send_message(note_off)
                        time.sleep(0.1)


        elif sig_value == 4:
            
            print("gyro-Z")
            print(value)
         
            
        elif sig_value == 5:
            #print(value)
            if gyroY is None: 
                gyroY = value
                continue
           
            if isRotatedBooleanYRight:
                if value < (gyroY + 3500):
                    isRotatedBooleanYRight = False
            elif value > (gyroY + 5000):
                isRotatedBooleanYRight = True

                if available_ports:
                    midiout.open_port(0)

                if editMode:
                    with midiout:
                        note_on = [0x90, 68, 112] # channel 1, middle A+1, velocity 112
                        note_off = [0x80, 68, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)
                else: 
                    with midiout:
                        note_on = [0x90, 66, 112] # channel 1, middle A+1, velocity 112
                        note_off = [0x80, 66, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)

                print("drehung rechts")
                print(value)

            if isRotatedBooleanYLeft:
                if value > (gyroY - 3500):
                        isRotatedBooleanYLeft = False
            elif value < (gyroY - 5000):
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
                        note_on = [0x90, 65, 112] # channel 1, middle A, velocity 0
                        note_off = [0x80, 65, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)
                    
                print("drehung Links")
                print(value)
                

        elif sig_value == 6:
            #print(value)
            if gyroZ is None: 
                gyroZ = value
                continue
           
            if isRotatedBooleanZRight:
                if value < (gyroZ + 3500):
                    isRotatedBooleanZRight = False
            elif value > (gyroZ + 5000):
                isRotatedBooleanZRight = True

                if available_ports:
                    midiout.open_port(0)

                if editMode:
                    if maxPitch == 52 and minPitch > 0: 
                        # von runtergepitcht auf normal
                        minPitch = 52
                        maxPitch = 65
                    else:
                        # von normal hoch pitchen
                        minPitch = 65
                        maxPitch = 76
                    with midiout:
                        for k in range(minPitch, maxPitch):
                            fader = [0xE0, 10, k]
                            midiout.send_message(fader)
                            midiout.send_message(fader)
                            time.sleep(0.01)

                else: 
                    with midiout:
                        note_on = [0x91, 71, 112] # channel 1, middle A+1, velocity 112
                        note_off = [0x81, 71, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)

                print("drehung rechts")
                print(value)

            if isRotatedBooleanZLeft:
                if value > (gyroZ - 3500):
                    isRotatedBooleanZLeft = False
            elif value < (gyroZ - 5000):
                isRotatedBooleanZLeft = True

                if available_ports:
                    midiout.open_port(0)

                if editMode:
                    if maxPitch == 76:
                        # von hochgepitcht auf normal
                        minPitch = 76
                        maxPitch = 63
                    else:
                        # von normal runter pitchen
                        minPitch = 63
                        maxPitch = 52
                    with midiout:
                        for k in range(minPitch, maxPitch, -1):
                            fader = [0xE0, 10, k]
                            midiout.send_message(fader)
                            midiout.send_message(fader)
                            time.sleep(0.01)

                else:
                     with midiout:
                        note_on = [0x91, 73, 112] # channel 1, middle A, velocity 0
                        note_off = [0x81, 73, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)
                    
                print("drehung Links")
                print(value)
            
        elif sig_value == 7:
            """
            print("bend")
            print(value)
            """
            if isPressed:
                if value < 190:
                    isPressed = False
                
            elif value > 210: 
                isPressed = True

                if available_ports:
                    midiout.open_port(0)

                    with midiout:
                        note_on = [0x90, 67, 112] # channel 1, high C, velocity 112
                        note_off = [0x80, 67, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.1)
                        midiout.send_message(note_off)
                
        else:
            print("!!!didnt match!!!")


del midiout        
        # flush serial for unprocessed data
        #ser.flushInput()
        #print("new command:", command)
        #if str(command) == '1':
        #    print("Playing movie")
        #    Popen('killall omxplayer.bin')
        #    Popen(['omxplayer','-b', movie1])
        #else:
        #    print("Not a valid command")


