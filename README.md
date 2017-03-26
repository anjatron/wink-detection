# wink-detection
Computer Vision project to create a program that can detect winks from images or video using OpenCV and Python.

SETUP AND DESIGN
----------------
Directories:
	posiris - positive images
	neg 	- negative images
	samples - sample images created
	cropped-files - cropped text files produced for each postive image
	OG 		- original cascade information for training 'winks'
	wink-images - test images
Files:
	DetectWink.py - main program
	Detect.py - test
	cascade.xml - pupil cascade
	params.xml - specified cascade parameteres
	cropped.vec - cropped vector file created from samples
	positives.txt - list of locations for pos images
	negatives.txt - list of location for neg images


DetectWink.py is the main program used for this project, I happened to leave Detect.py in this folder as well just for reference. 

My first approach was rather 'plug-and-play'. I went through Opencv's documentation and tutorials for Python that covered topics like histogram equalization, hough circles, smoothing, etc. By applying Histogram equalization to the entire gray scaled image first and then using the haar face cascade, I was able to pick up most of the faces in the wink-images folder other than two. Testing this on video also worked even though the video has horrible lagging problems. 
To detect winks I used the same eye cascade provided but I applied median blurring to the detected face before. This was a successful hit for 15 out of the 19 eyes detected. Now my main question was, how else can I try to pick up eyes? First I wanted to try to train my own cascade to see if I could detect pupils for faces without eyes from the first round of cascades. Unfortunately my own cascades did not add any improvement mainly because I didn't have enough positive images or time to train a large amount of samples. I still thought that trying to find pupils would be a good idea, and went about another route with some more opencv methods. After some research about object detection, I came across Opencv's Hough Circles method - part of which we covered in class. Time was once again an issue, but I realized that most of the faces with less that 5 hough circles detected were positive winking matches so if I counted those my success rate was perfect. This was not a valid enough educted guess so I commented out that logic to not give false readings. 
Video detection works really well with just the logic stated above. In fact the main problem with false readings is the consistent 'dropped camera frame' which cause DetectWink to lag places faces and eyes but corrects itself with enough time. 
Ideally I would have liked to have more time to train cascades better to detect pupils themselves. With enough accuracy it should do the trick in detect winks every time. Another option could be applying the golden ratio on the porportions of the face to detect where the eyes are, then playing with various smoothing and threshold techniques use hough circles to detect pupils. Something I also tried was cascade training for half of the face. Since it wasn't a bad approach still I wanted to only look at circles detected or run the eyes cascade on the top portion of the face only, so I passed around the faces location to make checks for the y-axis that are smaller than the y location of the face. 


RUNNING THE PROGRAM
--------------------

To run on a folder of images:
python DetectWink.py wink-images

To run on video:
python DetectWink.py


Both can be termintated with key input or ctrl c. 



CASCADE TRAINING COMMANDS
-------------------------
opencv_createsamples -img posiris/206110702_babecf94bf.jpg -bg negatives.txt -info crop1.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/beautiful-eyes-9.jpg -bg negatives.txt -info crop2.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/cs-eye-health-watery-eyes-722x406.jpg -bg negatives.txt -info crop3.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/dolly-iris.jpg -bg negatives.txt -info crop4.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/eyes-945248_960_720.jpg -bg negatives.txt -info crop5.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/eyes-brown.jpg -bg negatives.txt -info crop6.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/fringe-iris.JPG -bg negatives.txt -info crop7.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/imgres.jpg -bg negatives.txt -info crop8.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/Picture_of_brown_eyes.jpg -bg negatives.txt -info crop9.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

opencv_createsamples -img posiris/women-wink-iris.jpg -bg negatives.txt -info crop10.txt -num 10 -w 10 -h 20 -maxxangle 0 -maxyangle 0 -maxzangle 0 -bgcolor 255 -bgthresh 10

cat crop1.txt crop2.txt crop3.txt crop4.txt crop5.txt crop6.txt crop7.txt crop8.txt crop9.txt crop10.txt > crop.txt

opencv_createsamples -info crop.txt -vec cropped.vec -num 50 -w 10 -h 20

opencv_traincascade -data . -vec cropped.vec -bg negatives.txt -w 10 -h 20 -numPos 50 -numStages 10

