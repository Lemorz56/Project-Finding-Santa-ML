# Raspberry Pi Files
Theres quite alot of requirements for this to work. 
I *highly* suggest you install OpenCV by yourself before using this.

This contains a python file that i ran on my Raspberry Pi 3B. You have to have some sort of camera plugged in to be able to run this. I had a normal Logitech 720P Webcam connected through a USB slot.

There is a trained model included as well.


#### Create a virtual enviroment 
run `mkvirtualenv tomten -p python3`

#### Installing pip modules
run `pip install -r requirements.txt` to install the required pip modules. 
*I HIGHLY recommend installing OpenCV on your own!*

#### Run
`python not_santa_detector_rpi.py`
