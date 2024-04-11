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

There are two forms of Flash memory on the vape: internal Flash on the microcontroller, and 1 megabyte (8 megabits) of external SPI NOR Flash. The former contains the firmware, while the latter contains all the images that are displayed on the LCD, as well as the total time that the vape heating coil was in use; this counter is used to derive the number of "bars" displayed on the vape juice meter. Analysis of the LCD data bus (see the .dsl logic capture using [DreamSourceLab DSView](https://www.dreamsourcelab.com/download/)) suggests that the microcontroller uses DMA (Direct Memory Access) to stream image data from the external Flash into the LCD, as data transfers occur as contiguous 4096-byte chunks, corresponding to a single NOR Flash page.

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
  1. Some animation frames found in external Flash memory appear to be unused (and even reference the RAZ brand name), but could possibly be activated in firmware or somewhere else; this has not yet been researched.
  2. The juice meter value is derived from the vape timer, but the exact formula to derive it has not yet known. However, what is known is that it has no overflow protection and setting the value back to 0x00000000 will reset the juice meter.
  3. If Flash locations 0xF8000-0xF8004 are erased to 0xFF bytes, this flag byte will be reinitialized to 0xBB and the timer will be reinitialized to 0x00000000, also effectively resetting the juice meter. Additionally, any other bytes in this Flash sector will be clobbered to 0xFF, since a page erase is issued whenever the counter is updated; only the timer and flag bytes are preserved by the firmware.
  
## Resetting the Vape Juice Meter

As described in notes 2 and 3 above, filling external Flash locations 0xF8000-0xF8004 with 0xFF will reset the juice meter to full, permitting reuse of the vape once the reservoir is refilled. The microcontroller itself then needs to be reset by pulling the nRST pin to ground, or by power cycling it by disconnecting and reconnecting the battery; this will likely have already happened if one is desoldering and resoldering the external Flash for reprogramming/patching.
  
# External I/O

## SWD Debugging Port

The microcontroller uses the industry standard Serial Wire Debug (SWD) debug/programming interface for reading/writing its firmware and/or its internal SRAM memory. The SWD interface is exposed through the vape's USB-C charging port. The SWDIO/SWCLK lines are connected to the CC pins behind the normal 5.1k Rd pulldown resistors, as the connector is normally power-only.

The firmware on the microcontroller is not readout-protected, so further research into the firmware via decompilation is a possible avenue. It may be possible to use this debug interface to interact with the external Flash, but this has not been researched yet.

## UART Test Pads

Some of the vape mainboards that were tested, had RX/TX test pads on the backside of the board. This has not yet been researched, as to how this port interacts with the firmware, and/or if it can be used to update the external Flash contents.