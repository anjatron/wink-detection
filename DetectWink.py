# This is the main program for this project. It was built from the skeleton code given in the project prompt
# and modified to be able to detect more winks.


import cv2
import numpy as np
import os
import sys


totaleyes = 0 
totalfaces = 0
totalpupils = 0

# specify the haar face and eyes cascades
FACES_CASCADE_NAME =  '~/opencv/data/haarcascades/haarcascade_frontalface_alt.xml' 
EYES_CASCADE_NAME = '~/opencv/data/haarcascades/haarcascade_eye.xml' 
FACES_CASCADE =  cv2.CascadeClassifier(os.path.expanduser(FACES_CASCADE_NAME))
EYES_CASCADE = cv2.CascadeClassifier(os.path.expanduser(EYES_CASCADE_NAME))


# The cascade classifiers that come with opencv are kept in the following folder on my machine:
# build/data/haarscascades
def detectWink(frame, location, ROI_gray, ROI_color, cascade):
	global totaleyes, totalpupils

	# Approach:
	# 	- check center of eyes first 
	# 	- if it's below the center of the face then it's not an eye
	#	- if there are two eyes and one is below the other then there's only one eye

	blurred = cv2.medianBlur(ROI_gray, 3)
	eyes = cascade.detectMultiScale(blurred, 1.3, 5, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))


	eye_count = len(eyes)
	totaleyes += int(eye_count)

	# if no eyes are detected, check to see if pupils can be found
	if (eye_count == 0):
		# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
		# morph = cv2.morphologyEx(ROI_gray, cv2.MORPH_OPEN, kernel)
		# morph = cv2.dilate(ROI_gray, kernel, iterations = 5)
		# (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(morph)
		# print '(minVal, maxVal, minLoc, maxLoc):',(minVal, maxVal, minLoc, maxLoc)
		thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

		# laplacian = cv2.Laplacian(morph,cv2.CV_64F)

		# detect pupil
		circles = cv2.HoughCircles(thresh, cv2.cv.CV_HOUGH_GRADIENT, 2, 11, param1=75, param2=75, minRadius=0, maxRadius=0)

		if (circles is not None):
			circles = np.uint16(np.round(circles))

			totalpupils += len(circles[0])

			print 'circles found:', len(circles[0])

			# if (len(circles) <= 5):
			# 	eye_count = 1
				
			# for i in circles[0,:]:
			# 	if (i[1] > location[1]/3 and i[1] < location[1]/2):
			# 		# draw the outer circle
			# 		# cv2.circle(ROI_color, (i[0],i[1]), i[2], (0, 255, 0), 2)
			# 		# # draw center of the circle
			# 		# cv2.circle(ROI_color, (i[0],i[1]), 2, (0,0,255), 3)
		
		cv2.imshow('output', thresh)

	for (ex, ey, ew, eh) in eyes:
		ew2 = ew/2
		eh2 = eh/2

		# we want to look only at the section of the face that is above its center on the y axis
		if (ey < location[1]): 
			cv2.ellipse(ROI_color, (ex+ew2, ey+eh2), (ew2, eh2), 0, 0, 360, (255, 255, 0), 2, 8, 0)

	return (eye_count == 1)



def detect(frame, cascade_face, cascade_eyes):	
	global totalfaces

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# This is where I apply some CV methods to try and make detection more accurate
	histogram = cv2.equalizeHist(gray)

	faces = cascade_face.detectMultiScale(histogram, 1.1, 3, cv2.cv.CV_HAAR_SCALE_IMAGE, (30, 30))

	face_count = len(faces)
	totalfaces += int(face_count)

	detected = 0

	# find faces
	for (x, y, w, h) in faces:
		w2 = w/2
		h2 = h/2
		
		cv2.ellipse(frame, (x+w2, y+h2), (w2, h2), 0, 0, 360, (255, 0, 255), 2, 8, 0)

		roi_gray = histogram[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]

		# find eyes in faces
		if (detectWink(frame, (x+w2, y+h2), roi_gray, roi_color, cascade_eyes)):
			detected += 1


	# cv2.imshow('output', frame)

	return detected



# run wink detection program for live video
def runonVideo(faces_cascade, eyes_cascade):
	capture = cv2.VideoCapture(0)

	while 1:
		ret, frame = capture.read()

		detect(frame, faces_cascade, eyes_cascade)
		cv2.imshow('video', frame)

		key = cv2.waitKey(30) & 0xff

		# stop if user hits escape
		if key == 27:
			break

	capture.release()



# run wink detection program over a folder of static images
def runonFolder(faces_cascade, eyes_cascade, folder):
	
	if (folder[(len(folder) - 1)] != '/'):
		folder = '%s/' %(folder);

	directory = './%s' %(folder)
	# *check if directory is open
	detected = 0

	# go through every image in the directory 
	for filename in os.listdir(directory):
		if (filename != '.DS_Store'):
			print filename

			pathname = '%s%s' %(directory, filename)

			# read the image f
			image = cv2.imread(pathname, cv2.IMREAD_UNCHANGED)

			# start detecting winks!
			d = detect(image, faces_cascade, eyes_cascade)	
			detected += d

			cv2.imshow(filename, image) # Display the image

			key = cv2.waitKey(30) & 0xff

			if key == 27:
				break

	return detected



def main():
	global totaleyes, totalfaces

	foldername = ''
	argc = len(sys.argv)

	# check user input
	# if (argc != 1 or argc != 2):
	# 	print 'Error: you need to specify folder (2) or video (1)'
	# 	return -1

	if (argc == 2):
		foldername = sys.argv[1]

	detections = 0 # to keep track of wink detections

	if (argc == 2):
		# go through folder of images
		detections = runonFolder(FACES_CASCADE, EYES_CASCADE, foldername)
		print 'total detections:', detections
	else:
		# detect winks from live video
		runonVideo(FACES_CASCADE, EYES_CASCADE)

	print 'Total faces:', totalfaces
	print 'Total eyes:', totaleyes
	# pupils right now represent the total number of circles found in faces that had no eye matches
	print 'Total pupils:', totalpupils 

	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return 0






# START
if __name__ == '__main__':
	main()