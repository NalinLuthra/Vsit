from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
import numpy as np, cv2
from time import sleep

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def nothing(temp):
		pass

def cholesterol(sample):
	blur = cv2.medianBlur(sample,5)
	bil = cv2.bilateralFilter(blur,5,1000,1000)
	copy_orig = bil.copy()
	gray = cv2.cvtColor(bil,cv2.COLOR_BGR2GRAY)
	ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

	cv2.imshow('Masked Image', thresh1)

	# Trackbar for changing the threshold value.
	cv2.createTrackbar('min_value','Masked Image',0,255,nothing)

	# Trackbar execution.
	while(1):
		cv2.imshow('Masked Image', thresh1)

		min_value = cv2.getTrackbarPos('min_value', 'Masked Image')
		ret,thresh1 = cv2.threshold(gray,min_value,255,cv2.THRESH_BINARY_INV)

		# If ESC is pressed, execution breaks from the loop.
		k = cv2.waitKey(37)
		if k == 27:
			cv2.destroyAllWindows()
			break

	# Contour detection.
	contours, hierarchy = cv2.findContours(thresh1, 1, 2)
	cont = max(contours, key=cv2.contourArea)

	# Center and radius detection of pupil.
	(x,y), pupil_radius = cv2.minEnclosingCircle(cont)
	pupil_center = (int(x), int(y))
	pupil_radius = int(pupil_radius)
	cv2.circle(sample, pupil_center, pupil_radius, (0,0,255), 2)

	# Multiplier based on general ratio of radius of iris to pupil.
	iris_radius = pupil_radius*4

	# Radius detection for Iris.
	(cx,cy) = (int(x)+iris_radius, int(y))

	if cx > 640:
		cx = 640

	if cy > 640:
		cy = 640

	try:
		while(1):

			if cx > 639:
				color = gray[cy,cx]
				break
			color = gray[cy,cx]
			if color>110:
				cx = cx-1
			else:
				break

		iris_radius = cx-pupil_center[0]

	except:
		iris_radius = pupil_radius*4

	
	cv2.circle(sample,pupil_center,iris_radius , (0,0,255), 2)

	# Finding the minimum bounded rectangle.
	cv2.circle(sample,pupil_center,iris_radius , (255,255,255), -1)
	gray1 = cv2.cvtColor(sample,cv2.COLOR_BGR2GRAY)
	ret,thresh2 = cv2.threshold(gray1,250,255,cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh2, 1, 2)

	if len(contours)>0:
		maxC = max(contours, key=cv2.contourArea)
		x,y,w,h = cv2.boundingRect(maxC)
		cv2.rectangle(sample,(x,y),(x+w,y+h),(255,255,255),2)

	# Cropping to a standard size.
	cropped = copy_orig[y:y+h, x:x+w]
	cropped = cv2.resize(cropped, (240,240))

	mask = np.zeros(sample.shape, dtype = "uint8")
	cv2.circle(mask,pupil_center,iris_radius , (255,255,255), -1)
	cv2.circle(copy_orig, pupil_center, int(pupil_radius*2.2), (0,0,0), -1)
	mask = mask[y:y+h, x:x+w]
	mask = cv2.resize(mask, (240,240))
	mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	copy_orig = copy_orig[y:y+h, x:x+w]
	copy_orig = cv2.resize(copy_orig, (240,240))
	res = cv2.bitwise_and(copy_orig,copy_orig, mask = mask)

	##res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	##imga = np.asarray(res,dtype=np.float64)
	##pol = topolar(imga)
	# Output Image for nomarlized iris.
	##cv2.imshow('Normalize', pol)

	y, x = res.shape[:2]
	total = 0
	mat = 0
	for i in range(x):
		for j in range(y):
			arr = res[j, i]
			if (abs(arr[0]-arr[1])<=10) and (abs(arr[1]-arr[2])<=10) and (abs(arr[2]-arr[1]) <= 10):
				mat+=1
			total+=1

	ratio_of_grey = mat/total
	return ratio_of_grey

def camera(request):

	cam = cv2.VideoCapture(0)

	while True:
		ret, frame = cam.read()
		cv2.putText(frame, 'Press "q" to capture.',(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
		cv2.imshow('frame', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			sample = frame
			break

	cam.release()
	cv2.destroyAllWindows()

	cholesterol_level = cholesterol(sample)

	return HttpResponse('Camera done.')