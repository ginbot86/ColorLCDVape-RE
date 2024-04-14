# ColorLCDVape-RE
 Reverse-engineering of some rechargeable disposable vapes that include a small color TFT LCD (Raz/Kraze HD7K/etc.).
 
 Further updates can be found at https://github.com/ginbot86/ColorLCDVape-RE

# Introduction
Some disposable vapes on the market include accoutrements like a color LCD screen and USB-C rechargeability, yet are single-use throwaway devices; this makes such devices quite ecologically harmful. On the other hand, this opens up opportunities for hardware salvage by hobbyists/engineers, reusing the vape as-is by refilling it with fresh vape juice and resetting the internal meter, or even customization by editing the onboard images.

The specific vape being researched in this project comes by various names, but the one that was researched specifically was called the Kraze HD7K. However, this vape has also been seen under the "RAZ" brand name.

# Hardware

The vape uses the following hardware:

 - Nations Tech [N32G01K8Q7-1](https://www.nationstech.com/uploadfile/file/20220907/1662539811646982.pdf) microcontroller, featuring a 48MHz Arm Cortex-M0 core, 64k of internal Flash memory, 8k of SRAM
 - Giantech Semiconductor [GT25Q80A](https://uploadcdn.oneyac.com/upload/document/1676268194927_6539.pdf) 8Mbit (1Mbyte) SPI NOR Flash
 - LowPowerSemi [LP4068](https://pdf1.alldatasheet.com/datasheet-pdf/download/1244042/POWER/LP4068.html) linear Li-ion battery charger, configured for ~550mA charge current
 - LowPowerSemi LDO voltage regulator, labeled "LPS 2NDJ1" but exact model is unknown
 - Generic 5-pin SOT-23 vape controller, labeled "AjCH" with electret-type microphone sensing element
 - 0.96-inch 80x160 IPS TFT display, described below

# Display

The vape uses an 80x160 resolution 0.96-inch IPS LCD, with a 13-pin 0.7mm-pitch flat-flex (FPC) cable that is soldered to the vape mainboard. It connects via 4-wire SPI (data, clock, data/command, chip select), and appears to use the [ST7735S](https://www.displayfuture.com/Display/datasheet/controller/ST7735.pdf) controller. It even uses the same pinout for commercially available displays, like the [Smart Prototyping #102106](https://www.smart-prototyping.com/0_96-TFT-IPS-Bare-Display-ST7735-SPI-80-160).

## Display Pinout

| Pin | Name   | Function                              |
|-----|--------|---------------------------------------|
| 1   | TP0/NC | Unused                                |
| 2   | TP1/NC | Unused                                |
| 3   | SDIN   | SPI data to LCD                       |
| 4   | SCLK   | SPI clock                             |
| 5   | RS     | Logic low = command, high = data      |
| 6   | /RST   | Reset (active-low)                    |
| 7   | /CS    | Chip select (active-low)              |
| 8   | GND    | Power supply/signal ground            |
| 9   | NC     | Not connected                         |
| 10  | VDD    | Power supply (3.3V)                   |
| 11  | LEDK   | LED backlight cathode                 |
| 12  | LEDA   | LED backlight anode                   |
| 13  | GND    | Power supply/signal ground            |

# Flash Memory

There are two forms of Flash memory on the vape: internal Flash on the microcontroller, and 1 megabyte (8 megabits) of external SPI NOR Flash. The former contains the firmware, while the latter contains all the images that are displayed on the LCD, as well as the total time that the vape heating coil was in use; this counter is used to derive the number of "bars" displayed on the vape juice meter. Analysis of the LCD data bus (see the .dsl logic capture using [DreamSourceLab DSView](https://www.dreamsourcelab.com/download/)) suggests that the microcontroller uses DMA (Direct Memory Access) to stream image data from the external Flash into the LCD, as data transfers occur as contiguous 4096-byte chunks, corresponding to a single NOR Flash page. Analysis of the microcontroller's memory indicates that the DMA memory buffer lies in RAM addresses 0x2000022C-0x2000062B.

## External Flash Image Format

All images are stored on the external Flash as raw RGB565 16-bit bitmaps (i.e. each pixel takes up 2 bytes of data). Conversion tools, such as ImageConverter565 from Rinky-Dink Electronics' [UTFT library](http://www.rinkydinkelectronics.com/library.php?id=51), can be used to convert image formats like JPEG/PNG into a raw binary file that can be patched into the external Flash at the corresponding offset. There is no metadata stored with the raw images, so the image dimensions must be manually supplied, as shown in the table below.

## External Flash Memory Layout

| Index (#) | Offset (Hex) | Length (Hex) | Frame H (px) | Frame V (px) | Category                          | Unused? | Seq (#) | Notes |
| --------- | ------------ | ------------ | ------------ | ------------ | --------------------------------- | ------- | ------- | ----- |
| 0         | 0            | 6400         | 80           | 160          | Background                        |         | 0       |       |
| 1         | 6400         | 2880         | 72           | 72           | Battery Icon                      |         | 0       |       |
| 2         | 8C80         | 2880         | 72           | 72           | Battery Icon                      |         | 1       |       |
| 3         | B500         | 2880         | 72           | 72           | Battery Icon                      |         | 2       |       |
| 4         | DD80         | 2880         | 72           | 72           | Battery Icon                      |         | 3       |       |
| 5         | 10600        | 2880         | 72           | 72           | Battery Icon                      |         | 4       |       |
| 6         | 12E80        | 2880         | 72           | 72           | Battery Icon                      |         | 5       |       |
| 7         | 15700        | 2880         | 72           | 72           | Battery Icon                      |         | 6       |       |
| 8         | 17F80        | 2880         | 72           | 72           | Battery Icon                      |         | 7       |       |
| 9         | 1A800        | 2880         | 72           | 72           | Battery Icon                      |         | 8       |       |
| 10        | 1D080        | 2880         | 72           | 72           | Battery Icon                      |         | 9       |       |
| 11        | 1F900        | 2880         | 72           | 72           | Battery Icon                      |         | 10      |       |
| 12        | 22180        | 2880         | 72           | 72           | Juice Icon                        |         | 0       |       |
| 13        | 24A00        | 2880         | 72           | 72           | Juice Icon                        |         | 1       |       |
| 14        | 27280        | 2880         | 72           | 72           | Juice Icon                        |         | 2       |       |
| 15        | 29B00        | 2880         | 72           | 72           | Juice Icon                        |         | 3       |       |
| 16        | 2C380        | 2880         | 72           | 72           | Juice Icon                        |         | 4       |       |
| 17        | 2EC00        | 2880         | 72           | 72           | Juice Icon                        |         | 5       |       |
| 18        | 31480        | 2880         | 72           | 72           | Juice Icon                        |         | 6       |       |
| 19        | 33D00        | 6400         | 80           | 160          | Vaping Animation                  |         | 0       |       |
| 20        | 3A100        | 6400         | 80           | 160          | Vaping Animation                  |         | 1       |       |
| 21        | 40500        | 6400         | 80           | 160          | Vaping Animation                  |         | 2       |       |
| 22        | 46900        | 6400         | 80           | 160          | Vaping Animation                  |         | 3       |       |
| 23        | 4CD00        | 6400         | 80           | 160          | Vaping Animation                  |         | 4       |       |
| 24        | 53100        | 6400         | 80           | 160          | Vaping Animation                  |         | 5       |       |
| 25        | 59500        | 6400         | 80           | 160          | Vaping Animation                  |         | 6       |       |
| 26        | 5F900        | 6400         | 80           | 160          | Vaping Animation                  |         | 7       |       |
| 27        | 65D00        | 6400         | 80           | 160          | Vaping Animation                  |         | 8       |       |
| 28        | 6C100        | 6400         | 80           | 160          | Vaping Animation                  |         | 9       |       |
| 29        | 72500        | 6400         | 80           | 160          | Vaping Animation                  |         | 10      |       |
| 30        | 78900        | 6400         | 80           | 160          | Vaping Animation                  |         | 11      |       |
| 31        | 7ED00        | 6400         | 80           | 160          | Vaping Animation                  |         | 12      |       |
| 32        | 85100        | 6400         | 80           | 160          | Vaping Animation                  |         | 13      |       |
| 33        | 8B500        | 6400         | 80           | 160          | Vaping Animation                  |         | 14      |       |
| 34        | 91900        | 6400         | 80           | 160          | Vaping Animation                  |         | 15      |       |
| 35        | 97D00        | 6400         | 80           | 160          | Plugin Background 1               | Unused  | 16      | 1     |
| 36        | 9E100        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 0       | 1     |
| 37        | 9F8CA        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 1       | 1     |
| 38        | A1094        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 2       | 1     |
| 39        | A285E        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 3       | 1     |
| 40        | A4028        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 4       | 1     |
| 41        | A57F2        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 5       | 1     |
| 42        | A6FBC        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 6       | 1     |
| 43        | A8786        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 7       | 1     |
| 44        | A9F50        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 8       | 1     |
| 45        | AB71A        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 9       | 1     |
| 46        | ACEE4        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 10      | 1     |
| 47        | AE6AE        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 11      | 1     |
| 48        | AFE78        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 12      | 1     |
| 49        | B1642        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 13      | 1     |
| 50        | B2E0C        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 14      | 1     |
| 51        | B45D6        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 15      | 1     |
| 52        | B5DA0        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 16      | 1     |
| 53        | B756A        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 17      | 1     |
| 54        | B8D34        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 18      | 1     |
| 55        | BA4FE        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 19      | 1     |
| 56        | BBCC8        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 20      | 1     |
| 57        | BD492        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 21      | 1     |
| 58        | BEC5C        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 22      | 1     |
| 59        | C0426        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 23      | 1     |
| 60        | C1BF0        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 24      | 1     |
| 61        | C33BA        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 25      | 1     |
| 62        | C4B84        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 26      | 1     |
| 63        | C634E        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 27      | 1     |
| 64        | C7B18        | 17CA         | 35           | 87           | Logo Wipe                         | Unused  | 28      | 1     |
| 65        | C92E2        | 6400         | 80           | 160          | Plugin Background 2               | Unused  | 0       | 1     |
| 66        | CF6E2        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 0       | 1     |
| 67        | D0662        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 1       | 1     |
| 68        | D15E2        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 2       | 1     |
| 69        | D2562        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 3       | 1     |
| 70        | D34E2        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 4       | 1     |
| 71        | D4462        | F80          | 31           | 64           | Battery Bars Animation            | Unused  | 5       | 1     |
| 72        | D53E2        | 6400         | 80           | 160          | Plugin Background 3               |         | 0       |       |
| 73        | DB7E2        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 0       |       |
| 74        | DC67C        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 1       |       |
| 75        | DD516        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 2       |       |
| 76        | DE3B0        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 3       |       |
| 77        | DF24A        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 4       |       |
| 78        | E00E4        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 5       |       |
| 79        | E0F7E        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 6       |       |
| 80        | E1E18        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 7       |       |
| 81        | E2CB2        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 8       |       |
| 82        | E3B4C        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 9       |       |
| 83        | E49E6        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 10      |       |
| 84        | E5880        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 11      |       |
| 85        | E671A        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 12      |       |
| 86        | E75B4        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 13      |       |
| 87        | E844E        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 14      |       |
| 88        | E92E8        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 15      |       |
| 89        | EA182        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 16      |       |
| 90        | EB01C        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 17      |       |
| 91        | EBEB6        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 18      |       |
| 92        | ECD50        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 19      |       |
| 93        | EDBEA        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 20      |       |
| 94        | EEA84        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 21      |       |
| 95        | EF91E        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 22      |       |
| 96        | F07B8        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 23      |       |
| 97        | F1652        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 24      |       |
| 98        | F24EC        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 25      |       |
| 99        | F3386        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 26      |       |
| 100       | F4220        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 27      |       |
| 101       | F50BA        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 28      |       |
| 102       | F5F54        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 29      |       |
| 103       | F6DEE        | E9A          | 21           | 89           | Charger Logo Wipe                 |         | 30      |       |
| 104       | F8000        | 4            |  N/A         |  N/A         | Total Vape Time x0.01s (LSB->MSB) |         |  N/A    | 2     |
| 105       | F8004        | 1            |  N/A         |  N/A         | Vape In Use Flag (0xBB)           |         |  N/A    | 3     |

### Notes
  1. Some animation frames found in external Flash memory appear to be unused (and even reference the RAZ brand name despite the other branding showing Kraze), but could possibly be activated in firmware or somewhere else; this has not yet been researched.
  2. The juice meter value is derived from the vape timer, but the exact formula to derive it has not yet known. However, what is known is that it has no overflow protection and setting the value back to 0x00000000 will reset the juice meter.
  3. If Flash locations 0xF8000-0xF8004 are erased to 0xFF bytes, this flag byte will be reinitialized to 0xBB and the timer will be reinitialized to 0x00000000, also effectively resetting the juice meter. Setting the flag byte at 0xF8004 to anything that is not 0xBB will accomplish the same effect. Additionally, any other bytes in this Flash sector will be clobbered to 0xFF, since a page erase is issued whenever the counter is updated; only the timer and flag bytes are preserved by the firmware.

### Flash Dump Unpacking/Repacking, Customization Tools

Two Python scripts have been included to aid in splitting and reassembling the Flash dump into/from the individual images stored in the SPI Flash: ```split-flashdump.py``` and ```assemble-flashdump.py```. The tools currently do not perform format conversion (getting ChatGPT to help me this far was already a long process), but go a long way in aiding creation of custom "theme" packs. Unused resources can be removed from the repacked Flash dump by keeping them out of the directory containing the files to be reassembled; those unused regions will stay as 0xFF/erased bytes.

The repacker, ```assemble-flashdump.py```, expects the input filenames to be of a specific format, as it uses the hexadecimal-encoded offset to determine where to insert each piece into the 1MB Flash dump file (see split_map.csv or the included example theme, described below in *Custom Theme Packs*):

 - ```{index}_{offset}_{width}x{height}_{category}_{sequence}.bin```
 - Example: ```19_33d00_80x160_vapeanim-0.bin```

To convert PNG or JPEG images, use the previously-mentioned UTFT library's ```ImgConv.exe``` tool:
 - ```ImgConv.exe *.png /r```
 - ```ImgConv.exe *.jpg /r```
 - ```ren *.raw *.bin```
 
*Note: ensure the pictures to be converted into .bin format are the correct dimensions BEFORE converting them!*
 
### Custom Theme Packs

As a proof of concept, a finished Windows 95-style theme pack is included; it implements all resources for the battery and juice indicators, charging animation (only plugin background 3 and charger logo wipe, as that is the only used animation set with the tested firmware), and vaping animation (an aspect-ratio correct capture of the 3D Pipes screensaver). All that is needed is access to the SPI Flash and a means of reprogramming it. Room for extension of this concept could be through a cheap SWD USB dongle, connected through the USB-C port, and some software that uploads a small reprogramming tool into the microcontroller's RAM, potentially eliminating the need to desolder the Flash chip.

All of this customization is possible without touching the microcontroller's firmware!

## Resetting the Vape Juice Meter

As described in *External Flash Memory Layout*, notes 2 and 3 above, filling external Flash locations 0xF8000-0xF8004 with 0xFF will reset the juice meter to full, permitting reuse of the vape once the reservoir is refilled. The microcontroller itself then needs to be reset by pulling the nRST pin to ground, or by power cycling it by disconnecting and reconnecting the battery; this will likely have already happened if one is desoldering and resoldering the external Flash for reprogramming/patching.
  
# External I/O

## SWD Debugging Port

The microcontroller uses the industry standard Serial Wire Debug (SWD) debug/programming interface for reading/writing its firmware and/or its internal SRAM memory. The SWD interface is exposed through the vape's USB-C charging port. The SWDIO/SWCLK lines are connected to the CC pins behind the normal 5.1k Rd pulldown resistors, as the connector is normally power-only.

The firmware on the microcontroller is not readout-protected, so further research into the firmware via decompilation is a possible avenue. It may be possible to use this debug interface to interact with the external Flash, but this has not been researched yet.

## UART Test Pads

Some of the vape mainboards that were tested, had RX/TX test pads on the backside of the board. This has not yet been researched, as to how this port interacts with the firmware, and/or if it can be used to update the external Flash contents.

# Board-to-board Interconnect

The vape is made up of two PCBs, joined together with a 9-pin 0.15mm-pitch right-angle male pin header:

  1. Power board: USB-C interface, battery, vape controller with electret-type sensing element
  2. Logic board: LCD, battery charging, microcontroller, SPI Flash

## Interconnect Pinout

Pin 1 is denoted by a square pad on the power board, and a corresponding pad on the logic board's underside (opposite side of the microcontroller, SPI Flash and LCD). ***WARNING: The pin 1 markings may be opposite of each other between the two boards!***

| Power Board Pin | Logic Board Pin | Name      | Function                                                              |
|-----------------|-----------------|-----------|-----------------------------------------------------------------------|
| 1               | 9               | VBAT      | Battery positive (+) on power board                                   |
| 2               | 8               | VBUS      | +5V from USB-C port on power board with SMD fuse, "B" marking         |
| 3               | 7               | GND       | Power/signal ground                                                   |
| 4               | 6               | COIL_DRV  | Heater control signal from MCU on logic board (active-high)           |
| 5               | 5               | PUFF_DET  | Puff detection signal from power board vape controller (note 1)       |
| 6               | 4               | CC2/SWCLK | USB-C Rd pulldown 2 / SWD debug interface clock to MCU on logic board |
| 7               | 3               | CC1/SWDIO | USB-C Rd pulldown 1 / SWD debug interface data to MCU on logic board  |
| 8               | 2               | VDD       | 3V supply from LDO regulator on logic board to vape controller        |
| 9               | 1               | COIL_DET? | Heater coil detection to MCU on logic board (see note 2)              |

### Notes

  1. The puff detection signal seems to be a ~500Hz pulse train, either from the vape controller's LED driver output, or the heater output which might already be PWM'd for heater output. The lack of a "blink" when the 10 second timeout is exceeded suggests the latter.
  2. Pin 9/1 on the power/logic board header goes directly from the heater coil pin into a 5.1k/5.1k voltage divider on the logic board. Although currently unconfirmed, this might go to an ADC pin on the microcontroller to aid with load detection (a full Vbat reading could suggest that the heater coil is disconnected, and the vape animation will not play even if the vape controller is detecting a "puff").
  
# Firmware

The N32G01 series of microcontrollers are advertised in the datasheet as having onboard Flash encryption and secure boot support, but this feature (thankfully) is not used on the vape(s) tested so far (namely the Kraze HD7K).
  
## Firmware Dump

Not much work has gone into reverse-engineering the firmware itself, but a flash dump was able to be obtained with the use of a Segger J-Link and its corresponding J-Mem software, accessed through the SWD debug/programming port. Like many Arm-based MCUs, the Flash is located at 0x08000000 but is also mirrored at 0x00000000. A dump of the firmware was taken from addresses 0x08000000-0x0800FFFF (64k), and a cursory glance at the firmware dump shows that only approximately 50% of the Flash space was actually used (addresses from just before 0x8000 through 0xFFFF were all 0xFF bytes, indicating erased/unprogrammed memory). No human-readable strings appear to be present in the firmware dump.
  
## Firmware Version "Easter Egg(?)"

A "secret" version number is displayed on-screen if the USB-C power is rapidly turned on and off (but seems to occur inconsistently). When attempted with a Kraze HD7K, the screen turns black, and the text "GV-K23 0904V1" is displayed in red across two lines of text for a couple seconds; it appears to be rendered with a monospaced version of the 12-point-size "System" font from Windows. This hints to an internal product name of "GV-K23" and the firmware being revision 1, dated September 4, 2023. Coincidentally, near the end of the used Flash address space is a block of bytes filled with 0x00, and 0xE8E4, which looks suspiciously like black and red-orange pixel data. Further analysis of the raw data from this region confirms that the version number is stored as a raw bitmap and not rendered from a text string (explained below).
  
### Firmware Version Bitmap
Inside the firmware Flash dump, at addresses 0x7066-0x7E75, appears to be a bitmap version of the aforementioned version number. It appears to be only 60x30 pixels in size, but there are 0x00 padding bytes around this bitmap that do not align to 120-byte boundaries (60 pixels), making determining the "true" image size difficult without decompiling the firmware and finding the function that triggers the version screen.

#### Trademarks
All trademarks are the property of their respective owners.