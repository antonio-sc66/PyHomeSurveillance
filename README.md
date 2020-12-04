# PyHomeSurveillance
**This program is in a development stage**

Table of contents
=================
  * [Project objective](#project-objective)
  * [Structure](#structure)
  * [Requirements](#requirements)
  * [Objectives](#objectives)
  * [Contributing](#contributing)

## Project objective
This project implements a Python program designed to perform Home Surveillance with simple cameras (Webcams, Raspberry Pi ...).

## Licence
All the code and config files of this project are licenced under GPLv3.

## Requirements
### Hardware
Integrated camera, USB camera or CSI/MIPI Raspberry Pi camera

### Software
The project contains a requirements.txt with all the Python packages used.
The versions described the ones used during development and testing.

Virtual environments are recommended (virtualenv, Anaconda ...)

- Python3
- OpenCV
- Imutils
- Numpy

## Objectives
- [ ] Implement a detection system that can handle interior lighting conditions and exterior light interference
- [ ] Export video fragments when movement is detected
- [ ] Export a general log of the system
- [ ] Create an easy to use configuration file
- [ ] Mark the moving objects of the image to ease monitoring
- [ ] Perform object classification using CNNs in order to tag the moving element or to filter valid movements(example: exclude animals, cleaning robots ...)
- [ ] Allow easy backup of the exported files (could be as simple as copying the videos and logs to a file synchronization folder like Google Drive, Dropbox or OneDrive)

## Contributing
This project is open and welcomes contributions, create an issue with the proposals, bugs or questions.

If you want to submit code open a Pull Request against master and give clear indications about the proposed changes.