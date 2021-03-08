# USAGE
# python not_santa_detector.py 

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import clientClass
from imutils.video import VideoStream
from threading import Thread
import numpy as np
import imutils
import time
import cv2
import os
import ssl
import owncloud
import socket

# Config
import config

def sendAlarmTF(client, status):
	if(status == True):
		client.foundSanta()
	elif(status == False):
		client.noSanta()

def sendImageOC(oc, savePath, filePath):
	
	if filePath.endswith('.png'):
		oc.put_file(savePath, filePath)
		os.remove(filePath)
	
	

current_milli_time = lambda: int(round(time.time() * 1000))

#ip and port of server to connect to it
ip = config.ip
port = 15002

address = (ip, port)

# CA cert to verify server cert and clients own certs for server to verify client
client = clientClass.Client(address, "./CA.crt", "./client.crt", "./client.key")

# creating cloud connection and logging in
oc = owncloud.Client('http://192.168.1.169:8080')
oc.login(config.username, config.password)

# define the paths to the Not Santa Keras deep learning model and
# audio file
MODEL_PATH = "santa_not_santa.model"

# initialize the total number of frames that *consecutively* contain
# santa along with threshold required to trigger the santa alarm
TOTAL_CONSEC = 0
TOTAL_THRESH = 20

# initialize is the santa alarm has been triggered
SANTA = False

# load the model
print("[INFO] loading model...")
model = load_model(MODEL_PATH)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
    
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# prepare the image to be classified by our deep learning network
	image = cv2.resize(frame, (28, 28))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)


	# classify the input image and initialize the label and
	# probability of the prediction
	(notSanta, santa) = model.predict(image)[0]
	label = "Not Santa"
	proba = notSanta

	# check to see if santa was detected using our convolutional
	# neural network
	if santa > notSanta:
		# update the label and prediction probability
		label = "Santa"
		proba = santa
		# set name for the image
		filename = "./images/frame" + str(current_milli_time()) + ".png"
		

		# increment the total number of consecutive frames that
		# contain santa
		TOTAL_CONSEC += 1

		# check to see if we should raise the santa alarm
		if not SANTA and TOTAL_CONSEC >= TOTAL_THRESH:
			# indicate that santa has been found
			SANTA = True
			cv2.imwrite(filename,frame)
			client.foundSanta()
			#salarmThread = Thread(target=sendAlarmTF, args=(client,SANTA))
			#salarmThread.daemon = True
			#salarmThread.start()
			
			sendImageThread = Thread(target=sendImageOC, args=(oc, "SantaPics/frame"+ str(current_milli_time()) + ".png", filename))
			sendImageThread.daemon = True
			sendImageThread.start()

	# otherwise, reset the total number of consecutive frames and the
	# santa alarm
	else:
		TOTAL_CONSEC = 0
		SANTA = False
		client.noSanta()
		#salarmThread = Thread(target=sendAlarmTF, args=(client,SANTA))
		#salarmThread.daemon = True
		#salarmThread.start()

	# build the label and draw it on the frame
	label = "{}: {:.2f}%".format(label, proba * 100)
	frame = cv2.putText(frame, label, (10, 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()