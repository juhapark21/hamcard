# Ham radio card 
A small dashboard that displays propagation conditions with colored LEDs. 

<img width="675" height="385" alt="SS 2026-06-11 at 5 26 39 PM" src="https://github.com/user-attachments/assets/759ad37f-ee7c-4b13-a0d0-35c0ad0bc2ca" />
<img width="735" height="424" alt="SS 2026-06-11 at 5 27 05 PM" src="https://github.com/user-attachments/assets/12c4241a-de87-4d5c-8192-89d94e0d3a78" />
<img width="824" height="559" alt="SS 2026-06-11 at 5 27 47 PM" src="https://github.com/user-attachments/assets/f0d02b0c-f588-4976-a6f1-ed63b1ef59a9" />

## How to use 
Replace the placeholder values in the firmware with the SSID and password of your known wifi network. This makes it so that the microcontroller can connect to a network and access the weather data online.  

Assemble the PCB. Components are sized to be possible to hand-solder - A few components are through-hole for ease of hand-soldering.  

After assembling the PCB, flash the firmware onto the XIAO ESP32C3 ([instructions here](https://wiki.seeedstudio.com/xiao_esp32c3_with_micropython/)). 


Connect the ESP32 to a power source via USB-C and turn the power switch ON. The indicator light on the bottom right corner will turn on. 

As long as the board is connected to a network and a power source, it will update its data every hour and the indicator lights will change accordingly. 

LED indicator lights ordered by general severity: 
- Green: Good-Great
- Yellow: Fair
- Orange: Fair-Poor
- Red: Poor 

To turn off, turn the power switch OFF then disconnect the board from the power source. 

## Why 
Propagation info like this is like the weather report for radio nerds. It helps determine which bands you should work, or approximately how far your signal will reach. 

I initially made it because I wanted a fun useful business card. That idea got a bit out of hand (the thickness and power consumption of this does not make it very suitable to be used as a card), but I ended up with a nice physical dashboard showing useful weather information for amateur radio. 

Most existing dashboards are online, so I wanted this to be a physical object separate from tabs or apps on my computer. 

## Process 
The design and build process is documented in detail [here](https://fallout.hackclub.com/projects/3668). Even though this project was smaller-scale, it involved a lot of trial-and-error. 

## Credits  
Thank you Paul N0NBH for the solar-terrestrial [data](https://www.hamqsl.com/).  

## Zine page 
<img width="1410" height="2000" alt="Zine - radiocard" src="https://github.com/user-attachments/assets/b8361109-df76-443a-961b-b342f4dbc649" />
