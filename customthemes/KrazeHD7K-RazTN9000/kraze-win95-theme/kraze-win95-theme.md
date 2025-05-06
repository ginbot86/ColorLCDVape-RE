# Windows 95 Theme for Raz/Kraze HD7K Disposable Vape with Color LCD
### Version 1.0

## Description

A handmade custom "theme" pack that replaces all image resources on the Raz/Kraze HD7K's 1MB SPI Flash memory - no firmware changes required. Enjoy the nostalgia of the 3D Pipes screensaver, the classic teal desktop, and other fun animations!

This theme pack is part of a larger reverse-engineering project, located at https://github.com/ginbot86/ColorLCDVape-RE. It is intended to:

 - demonstrate how to manipulate the contents of the SPI Flash memory
 - demonstrate how to make custom theme packs that fit within the restrictions of the original firmware
 - showcase the "hackability" of so-called "disposable" vapes
 - offer a level of customization previously unachieved for such devices, as well as how some embedded devices manipulate and display image data

## Author

Theme pack designed by Jason Gin (https://github.com/ginbot86), April 2024.

## Installation

Copy the entire contents of ```bin/kraze-win95-theme-assembled.bin``` to the 1MB SPI Flash chip with a programmer tool of your choice. This may require hand-soldering tools, skills, and materials to do so (but stay tuned on that project - there should eventually be a way to use a simple Serial Wire Debug/SWD debugging dongle to upload custom themes, with no surface-mount rework skills required...).

## Acknowledgments

*Windows 95 is a trademark of Microsoft Corporation. This project is not affiliated with or endorsed by Microsoft Corporation. All trademarks and copyrighted materials belong to their respective owners.*