import time
import digitalio
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_dotstar

# The keycode sent for each button, optionally can be paired with a modifier key
# https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode
button_keycode = Keycode.KEYPAD_NUMLOCK
modifier_keycode = None # e.g. Keycode.RIGHT_ALT

GREEN = (0, 255, 0)

kbd = Keyboard(usb_hid.devices)

button = digitalio.DigitalInOut(board.D0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

print("Waiting for button press: keycode %s with modifiers %s" % (button_keycode, modifier_keycode))

while True:
    if not button.value: # pressed?
        with adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness = 1.0) as pixels:
            print("Button pressed")

            pixels[0] = GREEN

            if modifier_keycode is not None:
                kbd.press(button_keycode, modifier_keycode)
            else:
                kbd.press(button_keycode)

            while (not button.value):
                pass

            print("Button released")

            kbd.release_all()

    time.sleep(0.01)
