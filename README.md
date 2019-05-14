# G.R.R. - Geographic Roaming Robot
Robot (AlphaBot2-Pi) that autonomously creates maps, storing information that the robot recieves through its camera input.

## Instructions
1. Install the following dependencies listed below.
2. Download any of the SSD512 weights provided in [this repository](https://github.com/pierluigiferrari/ssd_keras). Make sure these weights are loaded in the directory.
3. Copy python files in the RaspberryPi folder into your Raspberry Pi.

## Testing G.R.R.
1. Run the control panel, and make sure your raspberry pi and laptop is connected to the same network.
2. Open terminal, and type in ``ssh pi@<raspberry pi's IP address>``.
3. Type in ``sudo python3 <where you stored the RaspberryPi files>/GRR.py`` and the robot should start moving. A few seconds later, the control panel should be able to pick up data coming from the robot.
4. When done, ``Ctrl+C`` in terminal should stop the robot.

## Dependencies
* Python 3.x
* Pandas
* Pillow
* Javafx
* Numpy
* Tensorflow
* Keras
* Imageio

## To Do List
* Starter Control Panel - May 17th, 2019
* Shortest Path Algorithm - May 20th, 2019
* Efficient Movement Algorithm - May 26th, 2019
* Map Viewer (.mppy) - May 29th, 2019
* Full Working Application (Control Panel & Robot) - June 3rd, 2019
* Full Documentation and Application - June 6th, 2019

## Flowchart (v1.5-Alpha)
![alt text](https://github.com/Magichanics/GRR-Pi/blob/be8724e657bfecf57ec7b9cd98e724eef330caae/curr_ver.png)

[v1.0-Alpha flowchart](https://github.com/Magichanics/GRR-Pi/blob/c3b9f0c6a45b725a5bf3c15971ff976d40f442e5/version_flowchart.png)

## Credits
* Developed by Jan Garong and Matteo Tempo
* [ssd_keras](https://github.com/pierluigiferrari/ssd_keras) created by Pierluigi Ferrari
* [Find Heading by using HMC5883L interface with Raspberry Pi using Python](http://www.electronicwings.com) created by electronicwings.
* [AlphaBot2.py](https://www.waveshare.com/) provided by waveshare.
