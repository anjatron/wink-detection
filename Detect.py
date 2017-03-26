import cv2
import os
import numpy as np


# The cascade classifiers that come with opencv are kept in the following folder on my machine:
# build/data/haarscascades

def detect():
	FACES_CASCADE_NAME =  '~/opencv/data/haarcascades/haarcascade_frontalface_alt.xml' 
	EYES_CASCADE_NAME = '~/Project2/cascade.xml' 

	FACES_CASCADE =  cv2.CascadeClassifier(os.path.expanduser(FACES_CASCADE_NAME))
	EYES_CASCADE = cv2.CascadeClassifier(os.path.expanduser(EYES_CASCADE_NAME))

	image = cv2.imread('./wink-images/Metropolis-Wink.jpg', cv2.IMREAD_UNCHANGED)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = FACES_CASCADE.detectMultiScale(gray, 1.3, 5, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))

	print 'faces:', len(faces)

	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = image[y:y+h, x:x+w]

		eyes = EYES_CASCADE.detectMultiScale(roi_gray)

		print 'eyes:', len(eyes)

		for (ex, ey, ew, eh) in eyes:
			cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

	cv2.imshow('output', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


# START
detect()