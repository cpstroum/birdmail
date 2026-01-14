import time
import gc
import board
import busio
import displayio
import digitalio
import random

from fourwire import FourWire
from adafruit_st7789 import ST7789
from adafruit_circuitplayground import cp

# ---- Display init (TFT Gizmo on Circuit Playground Bluefruit) ----
displayio.release_displays()

# Gizmo uses SCL/SDA pads for SPI signals
spi = busio.SPI(board.SCL, MOSI=board.SDA)

# Gizmo uses RX/TX for CS/DC
display_bus = FourWire(spi, command=board.TX, chip_select=board.RX)

# Prep the switch for the mailbox door
door = digitalio.DigitalInOut(board.A1)
door.switch_to_input(pull=digitalio.Pull.UP)


display = ST7789(
    display_bus,
    width=240,
    height=240,
    rowstart=80,              # critical for proper alignment
    backlight_pin=board.A3,   # critical to actually see it
    rotation=180,
)

root = displayio.Group()
display.root_group = root

BIRDS = [
    {"name": "Spotted Towhee",       "bmp": "/images/towhee.bmp",     "tone": "towhee"},
    {"name": "Black-capped Chickadee","bmp": "/images/chickadee.bmp", "tone": "chickadee"},
    {"name": "Northern Flicker",     "bmp": "/images/flicker.bmp",    "tone": "flicker"},
    {"name": "Steller's Jay",        "bmp": "/images/jay.bmp",        "tone": "jay"},
    {"name": "American Robin",       "bmp": "/images/robin.bmp",      "tone": "robin"},
]

# Keep these global so the file stays open while displayed
_bmp_file = None
_odb = None
_tilegrid = None

def show_bmp(path: str):

    global _bmp_file, _odb, _tilegrid

    if _tilegrid:
        root.pop()
    if _bmp_file:
        _bmp_file.close()

    gc.collect()

    _bmp_file = open(path, "rb")
    _odb = displayio.OnDiskBitmap(_bmp_file)
    _tilegrid = displayio.TileGrid(_odb, pixel_shader=displayio.ColorConverter())

    # center it
    _tilegrid.x = (240 - _odb.width) // 2
    _tilegrid.y = (240 - _odb.height) // 2

    root.append(_tilegrid)

# ---- Sound signatures ----
def chirp_towhee():
    cp.play_tone(880, 0.08); time.sleep(0.03)
    cp.play_tone(988, 0.08); time.sleep(0.05)
    for _ in range(7):
        cp.play_tone(1320, 0.03); time.sleep(0.01)

def chirp_chickadee():
    cp.play_tone(1047, 0.12); time.sleep(0.05)
    cp.play_tone(784, 0.16); time.sleep(0.08)
    for _ in range(5):
        cp.play_tone(1568, 0.02); time.sleep(0.015)

def chirp_flicker():
    # "CLEAR" style; one-syllable call with a downslur; deterministic
        cp.play_tone(1700, 0.08)   # "CLEE"
        cp.play_tone(950, 0.08)    # "urr"


def chirp_jay():
    # Sustained angry "SKRAA-kak" call; clear, repeatable, assertive

    def burst(freqs, tone_dur, gap):
        for f in freqs:
            cp.play_tone(f, tone_dur)
            time.sleep(gap)

    for _ in range(3):  # repetition is the anger
        # SKRAA
        burst(
            [1300, 1550, 1850, 2200, 2500, 2300, 2100, 1900, 1700],
            tone_dur=0.025,
            gap=0.004
        )

        time.sleep(0.06)

        # KAK
        burst(
            [2000, 1800, 1600],
            tone_dur=0.018,
            gap=0.003
        )

        time.sleep(0.18)

def chirp_robin():
    for pitch in (784, 880, 988, 880):
        cp.play_tone(pitch, 0.12); time.sleep(0.05)

def play_signature(kind: str):
    {
        "towhee": chirp_towhee,
        "chickadee": chirp_chickadee,
        "flicker": chirp_flicker,
        "jay": chirp_jay,
        "robin": chirp_robin,
    }[kind]()

def announce(i: int):
    show_bmp(BIRDS[i]["bmp"])
    play_signature(BIRDS[i]["tone"])

# ---- Main loop ----
index = 0
last_a = False
last_b = False

announce(index)

while True:
    # a = cp.button_a  # onboard button to cycle birds
    a = door.value   # True when door is released
    b = cp.button_b

    if a and not last_a:
        index = (index + 1) % len(BIRDS)
        announce(index)
        time.sleep(0.18)

    if b and not last_b:
        play_signature(BIRDS[index]["tone"])
        time.sleep(0.18)

    last_a = a
    last_b = b
    time.sleep(0.01)
    # print("door open:", (door.value)) # for debugging
    time.sleep(0.2)
