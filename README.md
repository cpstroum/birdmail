# birdmail

Birdmail is an offline, single-purpose ambient device that plays bird calls through the Circuit Playground Bluefruit’s onboard speaker while showing simple, non-text visuals on the TFT Gizmo. It's a tiny screen doing visuals and a speaker doing birds.


## What It Does
With each press to a snap action switch:
- Cycles through a set of bird calls local to the Pacific Northwest (each a short, recognizable tone sequence).
- Loads and displays images from `images/` on the TFT Gizmo (ST7789, 240×240).

## Hardware

- Adafruit Circuit Playground Bluefruit
- Adafruit TFT Gizmo (ST7789, 240×240)
- Onboard speaker
- 3d printed mailbox modified from a publicly-shared stl, email me for it)

The TFT Gizmo is mounted using the standard standoffs and pogo pins. The switch is screwed to GND (C) and A1 (NO).

## Software

- CircuitPython
- Mu editor
- Core libraries: `displayio`, `adafruit_st7789`
- Audio: typically `simpleio` for `tone()` or `audiopwmio`/`audiocore` depending on your implementation

## Repo Layout

- `code.py`  
  Main program; selects an image + matching call; handles pacing.
- `images/`  
  Pre-rendered 240×240 assets shown on the TFT.  
  Keep file sizes reasonable; storage and RAM are limited.
- `lib/`  
  Required CircuitPython libraries (ST7789 driver and any helpers).
- `settings.py` / `birds.py` (optional, if present)  
  Mappings of image filenames to bird-call tone sequences.

## Images

Birdmail expects display assets to live in `images/`. Each scene is loaded from disk and shown full-screen.

Guidelines:
- Target size: 240×240 pixels.
- Prefer formats that CircuitPython can load efficiently on your board (BMP is common for `displayio.OnDiskBitmap`).
- Keep palettes and bit depth modest when possible.
- Filenames should match whatever mapping the code uses (for example, `flicker.bmp` paired to the flicker call).

### Audio

- Bird calls are encoded as short sequences of tones (frequency + duration).
- Playback is kept brief so the device stays responsive and visuals can keep updating.

## Installing

1. Install CircuitPython on the Circuit Playground Bluefruit (for me this was `adafruit-circuitpython-circuitplayground_bluefruit-en_US-10.0.3.uf2`)
2. Copy entirety of this repo into the root of `CIRCUITPY`

## Extending Birdmail

- Add a new bird call by defining a new tone sequence.
- Add a matching visual by creating a new `displayio.Group` scene or swapping bitmaps/palettes.
- Keep visuals non-text and lightweight; prioritize strong silhouettes and repeatable motifs.

## Constraints and Intentional Choices

- Fixed resolution: 240×240
- Fixed rotation (as used in your known-good TFT Gizmo setup)
- No NeoPixels
- No sensors or motion input
- No on-screen text

## Credits / Notes

Built for a proven Circuit Playground Bluefruit + TFT Gizmo stack. Designed for repeatable delight: short calls, crisp visuals, no internet dependencies.
