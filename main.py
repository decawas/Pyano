import time
import pygame.midi
import pyautogui
import json

def mouse(data, profile, keynum, velocity):
    if data["profiles"][0][profile][0][str(keynum)]["x"] == "v":
        x = velocity
    else:
        x = int(data["profiles"][0][profile][0][str(keynum)]["x"])

    if data["profiles"][0][profile][0][str(keynum)]["y"] == "v":
        y = velocity
    else:
        y = int(data["profiles"][0][profile][0][str(keynum)]["y"])
    
    if data["profiles"][0][profile][0][str(keynum)]["pn"][0] == "-":
        x -= (2 * x)
    if data["profiles"][0][profile][0][str(keynum)]["pn"][1] == "-":
        y -= (2 * y)
    
    return x, y

profile = "minecraft"
f = open("profiles.json")
data = json.loads(f.read())
f.close

pyautogui.FAILSAFE = False

midi_str = ''
pygame.midi.init()
num_midi_devices = pygame.midi.get_count()
print("-----------------")
print(num_midi_devices)

for m in range(0, num_midi_devices):
    print("Device Number: ", m, " ----------------------- ")
    print(str(pygame.midi.get_device_info(m)))

midiInput = pygame.midi.Input(3)

while True:
    while not pygame.midi.Input.poll(midiInput):
        time.sleep(.01)

    midi_data = pygame.midi.Input.read(midiInput, 1)
    midi_note, timestamp = midi_data[0]
    note_status, keynum, velocity, unused = midi_note
    keynum = str(keynum)
    print("Midi Note: \n\tNote Status: ", note_status, " Key Number: ", keynum, " Velocity: ", velocity, "\n\tTime Stamp: ", timestamp)
    try:
        if timestamp >= 10 and velocity > 5:
            key_down = True
            # hold key down
            print("a", data["profiles"][0][profile][0][keynum]["mo"])
            if data["profiles"][0][profile][0][keynum]["mo"] == "to":
                pyautogui.keyDown(data["profiles"][0][profile][0][keynum]["x"])
                print(data["profiles"][0][profile][0][keynum]["x"])

            # tap key
            elif data["profiles"][0][profile][0][keynum]["mo"] == "ta":
                pyautogui.keyDown(data["profiles"][0][profile][0][keynum]["x"])
                pyautogui.keyUp(data["profiles"][0][profile][0][keynum]["x"])

            # left click
            elif data["profiles"][0][profile][0][keynum]["mo"] == "lcl":
                pyautogui.mouseDown(x=0, y=0)
            
            # right click
            elif data["profiles"][0][profile][0][keynum]["mo"] == "rcl":
                pyautogui.mouseDown(button='right', x=0, y=0)
            
            # move mouse relative
            elif data["profiles"][0][profile][0][keynum]["mo"] == "mv":
                x, y = mouse(data, profile, keynum, velocity)
                pyautogui.move(x, y)
            
            # move mouse static
            elif data["profiles"][0][profile][0][keynum]["mo"] == "mu":
                x, y = mouse(data, profile, keynum, velocity)
                pyautogui.moveTo(x, y)
            
            # scroll
            elif data["profiles"][0][profile][0][keynum]["mo"] == "sc":
                xb, yb = mouse(data, profile, keynum, velocity)
                pyautogui.hscroll(xb, x=0, y=0)
                pyautogui.vscroll(yb, x=0, y=0)
            
        elif timestamp >= 10 and velocity <= 5: 
            key_down = False
            # hold key up
            if data["profiles"][0][profile][0][keynum]["mo"] == "to":
                pyautogui.keyUp(data["profiles"][0][profile][0][keynum]["x"])
            
            # left click release
            elif data["profiles"][0][profile][0][keynum]["mo"] == "lcl":
                pyautogui.mouseUp(x=0, y=0)
            
            # right click release
            elif data["profiles"][0][profile][0][keynum]["mo"] == "rcl":
                pyautogui.mouseUp(button='right', x=0, y=0)
        else:
            print("Unknown status!")
    except KeyError:
        pass
