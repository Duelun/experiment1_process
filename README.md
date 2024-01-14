I am make experiments to prove my Dual Element Universe theory. To this, I designed an electronic twin-board device. The device can take five different type electrical impulses on five channels at the exactly same time on twin-panels. By doing so, I can determine the difference between the fload rate of time in two different spatial locations and hopefully prove the existence of the ether.
The device directed by a Rapsberry Pi 4 micro-computer. This script runs on Raspberry Pi 4 and handle the device and saves the measurement datas.
The presented script can handle the saved datas.
The script was published to check the correctness of the measurement methodology.

![alt text](https://github.com/duelun/experiment1_save/blob/main/pictures/pic1.png?raw=true)
<picture>
 <img alt="electric-board" src="https://github.com/duelun/experiment1_save/blob/main/pictures/pic1.png">
</picture>


The operation of the script:
 - It start the run of electrical boards, measurer periferias and null the registers.
 - At the set time the script close the lach gates at same time on both circual board.
 - Read out and store the 2 x 48 bit datas and temperature sensors values.
 - Open the lach gates.
 - After the preset number of measuring stops the device and saves the struktured datas into file.
 - 
![alt text](https://github.com/duelun/experiment1_save/blob/main/pictures/pic2.png?raw=true)

The abilities of script:
 - Setable warming time. The electrical boards and periferias run without meassuring to warming up them at the working temperature.
 - Setable measurement interval. The devices has stable working from 0.1 s measuring interval. /without data showing/
 - Setable measuring number.
 - Setable continous measurment set number.
 - Showing data values and data grafs. /switchable/
 - 
![alt text](https://github.com/duelun/experiment1_save/blob/main/pictures/pic3.png?raw=true)
 
