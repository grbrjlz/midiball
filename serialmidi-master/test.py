
import time
import rtmidi
from subprocess import Popen
import serial

movie1 = "/home/pi/Videos/test.mp4"

ser = serial.Serial('/dev/cu.usbmodem142101',9600)
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)
gyroY = None
while True:

    command = ser.readline()

    
    #sig_value = command[-1] - 48
    #sig_value = str(command)
    if command:
        sig_value = int(command)
        value = int(ser.readline())
        #print("sigvalue: " + sig_value)
        if sig_value == 0:
            
            print("Button 1 klick")
            print("buttonValue: " + str(value))
            
            
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
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            
        elif sig_value == 2:
            print("Button 3 klick")
            print("buttonValue: " + str(value))
            
            if available_ports:
                midiout.open_port(0)
                with midiout:
                    note_on = [0x90, 62, 112] # channel 1, middle E, velocity 112
                    note_off = [0x80, 62, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            
        elif sig_value == 3:
            ## hoch runter beschleunigen
            print("gyro-Y")
            print(value)
    
            """
            if available_ports:
                midiout.open_port(0)
                with midiout:
                    note_on = [0x90, 63, 112] # channel 1, middle F, velocity 112
                    note_off = [0x80, 63, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            """
        elif sig_value == 4:
            ## vor zurück beschleunigen
            print("gyro-Z")
            print(value)
            
            """
            if available_ports:
                midiout.open_port(0)
                with midiout:
                    note_on = [0x90, 64, 112] # channel 1, middle G, velocity 112
                    note_off = [0x80, 64, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            """
        elif sig_value == 5:
            
            ## vor zurück neigen
            ##print("(eigentlich gyro-y) acc-Y")
            ##print(value)
            if gyroY is None: 
                gyroY = value
                continue

            if value < (gyroY - 12000):
                print("min")
                if available_ports:
                    midiout.open_port(0)

                with midiout:
                    note_on = [0x90, 65, 1] # channel 1, middle A, velocity 0
                    note_off = [0x80, 65, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)

            if value > (gyroY + 12000):
                print("max")
                with midiout:
                    note_on = [0x90, 65, 112] # channel 1, middle A, velocity 112
                    note_off = [0x80, 65, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            if value > (gyroY + 1500):
                print("drehung rechts")
                print(value)
            elif value < (gyroY - 1500):
                print("drehung links")
                print(value)
                ## gyroY min / velocity min
                ## -12.000 = 0
                ## gyroY max / velocity max
                ## +12.000 = 112

            """
            if available_ports:
                midiout.open_port(0)

                with midiout:
                    note_on = [0x90, 65, 112] # channel 1, middle A, velocity 112
                    note_off = [0x80, 65, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            """

        elif sig_value == 6:
            ## rechts links neigen
            print("acc-Z")
            print(value)
            
            """
            if available_ports:
                midiout.open_port(0)
                with midiout:
                    note_on = [0x90, 66, 112] # channel 1, middle H, velocity 112
                    note_off = [0x80, 65, 0] 
                    midiout.send_message(note_on)
                    time.sleep(0.5)
                    midiout.send_message(note_off)
                    time.sleep(0.1)
            """
            
        elif sig_value == 7:
            ## bend sensor winkel
            print("bend")
            print(value)
            if value > 500:
                
                if available_ports:
                    midiout.open_port(0)
                    with midiout:
                        note_on = [0x90, 67, 112] # channel 1, high C, velocity 112
                        note_off = [0x80, 67, 0] 
                        midiout.send_message(note_on)
                        time.sleep(0.5)
                        midiout.send_message(note_off)
                        time.sleep(0.1)
                
            
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


