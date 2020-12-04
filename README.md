# LicensePlateRec
![Python Basic Build test](https://github.com/grzes5003/LicensePlateRec/workflows/Python%20Basic%20Build%20test/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
> OpenCV in python 
 
License plate recognition and classification software

## Architecture overview
![alt text](https://github.com/grzes5003/LicensePlateRec/blob/ml-flexing/readme/Arch_diagram.png)
The project's architecture is relatively simple, but also scalable and reliable.
It is based on the **Mediator** pattern, therefore direct communications between the objects are restricted and forced to
go through the mediator object. Using of this design pattern eliminates the need for complex object-to-object communication schemes.
The **Mediator** interface declares methods of communication with components, which usually include just a single notification method. 

Classes structure:
* Manager - This class is so called **mediator** so it supervises all the other classes and controls its indirect communications.
Additionally, its responsibility is to created and watch *Thread and Process pools*. Each class component has a reference to the single 
instance of Manager class.

* ImgProcess - In order to verify and preprocess video file Image Process class is used. It verifies if input data type is correct and 
samples the video into Frame data-class objects, which then are passed to the Manager.

* ImgAnalize - Image analize class is responsible for extracting information from an image, which comes in a form of Frame class object.
It features C++ written ML library, which structure is described below, and returns JSON as a response. Based on JSON it creates LicensePlate
data-class object and adds it to the frame class, then passes it to the Manager.

* Frame - Trivial data class which is used for storing data regarding sample-frames.

* LicensePlate - Data class for storing information regarding license plates and its position on an image.

* OutGen, LogGen, VideoGen - These classes are responsible for the output, in a form of text logs and modified video.
## Machine Learning algorithm overview
![alt text](https://github.com/grzes5003/LicensePlateRec/blob/ml-flexing/readme/ML_diagram.png)
