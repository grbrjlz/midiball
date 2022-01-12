import time
import rtmidi
from subprocess import Popen
import serial

movie1 = "/home/pi/Videos/test.mp4"

ser = serial.Serial('/dev/cu.usbmodem141201',9600)
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

while True:
    command = ser.read()
    sig_value = command[-1] - 48
    if command:
        print(sig_value)
        if sig_value == 0:
            if available_ports:
                midiout.open_port(0)
        else:
            midiout.open_virtual_port("My virtual output")

        with midiout:
            note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
            note_off = [0x80, 60, 0]
            midiout.send_message(note_on)
            time.sleep(0.5)
            midiout.send_message(note_off)
            time.sleep(0.1)

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


