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
* **Manager** - This class is so called **mediator** so it supervises all the other classes and controls its indirect communications.
Additionally, its responsibility is to created and watch *Thread and Process pools*. Each class component has a reference to the single 
instance of Manager class.

* **ImgProcess** - In order to verify and preprocess video file Image Process class is used. It verifies if input data type is correct and 
samples the video into Frame data-class objects, which then are passed to the Manager.

* **ImgAnalize** - Image analize class is responsible for extracting information from an image, which comes in a form of Frame class object.
It features C++ written ML library, which structure is described below, and returns JSON as a response. Based on JSON it creates LicensePlate
data-class object and adds it to the frame class, then passes it to the Manager.

* **Frame** - Trivial data class which is used for storing data regarding sample-frames.

* **LicensePlate** - Data class for storing information regarding license plates and its position on an image.

* **OutGen, LogGen, VideoGen** - These classes are responsible for the output, in a form of text logs and modified video.
## Machine Learning algorithm overview
![alt text](https://github.com/grzes5003/LicensePlateRec/blob/ml-flexing/readme/ML_diagram.png)

License plate recognition algorithm operates as a pipeline. The input is an image in bytes format, then it goes through 
few consecutive stages of preprocess and ML models, as an output the algorithm presents license plate candidates found on the image.

Pipeline stages go as following:
* **Detection.** There is no point in processing the whole image, so the first stage (featuring Convolutional Neural Network) 
is designed to find region-candidates where plates could be. Each of these regions is sent to the later pipeline phases for further processing.
![alt text](https://github.com/grzes5003/LicensePlateRec/blob/ml-flexing/readme/detection.png)

* **Binarization.** This phase (and all subsequent phases) will occur multiple times — once for each possible license plate region.
Binarization is used in order to reduce unnecessary  color dimension. Additionally, few image distortions are applied so to maximise
chances of finding all the characters.
![alt text](https://github.com/grzes5003/LicensePlateRec/blob/ml-flexing/readme/binarization.png)

* **Normalization.** This stage will re-map the plate region to a standard size and orientation. 
Ideally, this will produce a correctly oriented plate image without rotation or skew.

* **Character segmentation.** The goal of this phase is to isolate and clean up the characters so that they can be processed individually.
![alt text](https://github.com/grzes5003/LicensePlateRec/blob/ml-flexing/readme/segmentation.png)

* **Character recognition.** The CR phase will analyze each character independently featuring Tesseract OCR by Google.
 For each character image, it will compute all possible characters and their confidences.
 
* **Edge search.** In this phase, the edges of the license plate will be searched for. 
 It is essential that the detection phase will only be responsible for identifying a possible region in which a license plate may exist. 
 So to separate plate itself from the region this stage is used.
 ![alt text](https://github.com/grzes5003/LicensePlateRec/blob/ml-flexing/readme/edge.png)

* **Postprocess.** Given a list of all possible OCR characters and confidences, post processing will determine the best possible plate letter combinations.
It will organize candidates list and then apply *regex* expressions in order to filter out the results. 