from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
import numpy as np, cv2, os, imutils
from statistics import mode
from tkinter import *
#from . import NameForm


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def direct_test(request):
    return render(request, 'direct_text.html')

def login(request):
    if 'Username' and 'Password' in request.GET:
        username = request.GET['Username']
        password = request.GET['Password']
        
    else:
        return HttpResponse('Empty fields. KIndly resubmit form.')

    return HttpResponse(str(username + "   " + password))

def signup(request):
    if 'emailid' and 'username' and 'date' and 'phone' and 'password' and 'confirmpass' in request.GET:
        emailid = request.GET['emailid']
        username = request.GET['username']
        date = request.GET['date']
        phone = request.GET['phone']
        password = request.GET['password']
        confirmpass = request.GET['confirmpass']

        if password != confirmpass:
            return HttpResponse('Incorrect password! Retry.')
        
    else:
        return HttpResponse('Empty fields. Kindly resubmit form.')

    return HttpResponse(str(emailid) + "   " + str(username)+str(date) + "   " + str(phone)+str(password) + "   " + str(confirmpass))

def aadhar(request):   

    from tkinter import filedialog

    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()

    if file_path is not "" and (".png" in file_path or ".jpeg" in file_path or ".jpg" in file_path or ".JPG" in file_path or ".PNG" in file_path):
        return HttpResponse('Aadhar done.')

    else:
        return HttpResponse('Failed. Please upload the right file.')

def aadhar2(request):
    try:
        camera=cv2.VideoCapture(1)
    except:
        camera = cv2.VideoCapture(0)

    while True:

        ret, frame = camera.read()
        cv2.putText(frame,'Press "ESC" to capture.',(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow("frame",frame)
        
        #cv2.imshow("eye",image)
        if cv2.waitKey(30)==27 & 0xff:
            ret, sample = camera.read()
            break

    camera.release()
    #print ("accurracy=",(float(numerator)/float(numerator+denominator))*100)
    cv2.destroyAllWindows()

    return HttpResponse('Photo clicked.')
    

def search_form(request):
    return render(request, 'search-form.html')

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm.NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm.NameForm()

    return render(request, 'name.html', {'form': form})

def nothing(temp):
    pass

def camera():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    face_cascade = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'haarcascade_frontalface_alt.xml'))

    try:
        camera=cv2.VideoCapture(1)
    except:
        camera = cv2.VideoCapture(0)

    numerator=0
    denominator=0

    pupil = []

    while True:

        ret, frame = camera.read()
        frame_copy = frame
        roi=frame
        frame=cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        coordinates_eye = []

        for (x,y,w,h) in faces:
            coordinates_eye.append((x,y,w,h))
    ##        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
            #cv2.line(frame,(int(x+w/2),int(y)),(int(x+w/2),int(y+h/2)),(255,0,0),1)
            #cv2.line(frame,(int(x+w/4.2),int(y+h/2.2)),(int(x+w/2.5),int(y+h/2.2)),(0,255,0),1)
            #cv2.line(frame,(int(x+w/4.2),int(y+h/3)),(int(x+w/2.5),int(y+h/3)),(0,255,0),1)
            cv2.line(frame,(int(x+w/4.2),int(y+h/3)),(int(x+w/4.2),int(y+h/2.2)),(0,255,0),1) #left
            cv2.line(frame,(int(x+w/2.5),int(y+h/3)),(int(x+w/2.5),int(y+h/2.2)),(0,255,0),1) #right
            
            #------------ estimation of distance of the human from camera--------------#
            d=10920.0/float(w)

            #-------- coordinates of interest --------------# 
            x1=int(x+w/4.2)+1       #-- +1 is done to hide the green color
            x2=int(x+w/2.5)
            y1=int(y+h/3)+1
            y2=int(y+h/2.2)
            roi=frame[y1:y2,x1:x2]
            gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            equ = cv2.equalizeHist(gray)
            thres=cv2.inRange(equ,0,20)
            kernel = np.ones((3,3),np.uint8)
            #/------- removing small noise inside the white image ---------/#
            dilation = cv2.dilate(thres,kernel,iterations = 2)
            #/------- decreasing the size of the white region -------------/#
            erosion = cv2.erode(dilation,kernel,iterations = 3)
            #/-------- finding the contours -------------------------------/#
            contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            #--------- checking for 2 contours found or not ----------------#
            if len(contours)==2 :
                numerator+=1
                #img = cv2.drawContours(roi, contours, 1, (0,255,0), 3)
                #------ finding the centroid of the contour ----------------#
                M = cv2.moments(contours[1])
                #print M['m00']
                #print M['m10']
                #print M['m01']
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    pupil.append((cx,cy))
                    cv2.line(roi,(cx,cy),(cx,cy),(255,0,255),10)
                    
                #print cx,cy
            #-------- checking for one countor presence --------------------#
            elif len(contours)==1:
                numerator+=1
                #img = cv2.drawContours(roi, contours, 0, (0,255,0), 3)

                #------- finding centroid of the countor ----#
                M = cv2.moments(contours[0])
                if M['m00']!=0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    pupil.append((cx,cy))
                    #print cx,cy
                    cv2.line(roi,(cx,cy),(cx,cy),(0,0,255),20)
        
            else:
                denominator+=1
                #print "iris not detected"            
    
        cv2.putText(frame,'Press "ESC" to capture.',(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow("frame",frame)
        
        #cv2.imshow("eye",image)
        if cv2.waitKey(30)==27 & 0xff:
            ret, sample = camera.read()
            break
    camera.release()
    #print ("accurracy=",(float(numerator)/float(numerator+denominator))*100)
    cv2.destroyAllWindows()

    x2 = 0
    y2 = 0

    try:
        a = mode([x for x in range(len(pupil))])

        for i in range(len(pupil)):
            if pupil[i][0] - a[0] > 20 or pupil[i][1] - a[1]>20:
                 pupil.remove(i+1)

     except:
        pass

    for index in range(len(pupil)):

            x2+= pupil[index][0]
            y2+= pupil[index][1]


    cx, cy = 0,0
    cx = x2/len(pupil)
    cy = y2/len(pupil)

    return sample,x2,y2

def cholesterol(sample, cx,cy):
    sample = imutils.resize(sample, width=640)
    blur = cv2.medianBlur(sample,5)
    bil = cv2.bilateralFilter(blur,5,1000,1000)

    y = cy-23
    h = 50
    x = cx - 60
    w = 110

    gray = cv2.cvtColor(bil,cv2.COLOR_BGR2GRAY)

    # Center and radius detection of pupil.
    pupil_center = (cx, cy)
    pupil_radius = 5
    cv2.circle(sample, pupil_center, pupil_radius, (0,0,255), 2)

    # Multiplier based on general ratio of radius of iris to pupil.
    iris_radius = pupil_radius*4
    
    cv2.circle(sample,pupil_center,iris_radius , (0,0,255), 2)

    # Finding the minimum bounded rectangle.
    cv2.circle(sample,pupil_center,iris_radius , (255,255,255), -1)

    # Cropping to a standard size.

    mask = np.zeros(sample.shape, dtype = "uint8")
    cv2.circle(mask,pupil_center,iris_radius , (255,255,255), -1)
    mask = mask[y:y+h, x:x+w]
    mask = cv2.resize(mask, (240,240))
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    copy_orig = copy_orig[y:y+h, x:x+w]
    copy_orig = cv2.resize(copy_orig, (240,240))
    res = cv2.bitwise_and(copy_orig,copy_orig, mask = mask)

    cv2.imshow("a", res)
    cv2.imshow("abb", sample)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
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

    #return ratio_of_grey
    return 20

def bilirubin(sample, cx,cy):
    image = imutils.resize(sample, width=640, height=480)
    image = cv2.medianBlur(image,5)
    image = cv2.bilateralFilter(image,5,1000,1000)
   # image = image[c] TODO
    frame = image.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([20,50,120]) #all shades of yellow
    upper_red = np.array([60,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask = mask)
    image = res.copy()
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    y, x = res.shape[:2]
    total = 0
    mat = 0
    for i in range(x):
        for j in range(y):
            arr = res[j, i]
            if arr == 0:
                continue
            mat+=1
            total+=arr

    average = float(total)/float(mat)
    average = 1- np.interp(average, [0,255], [0,1])
    cv2.imshow("gray", res)
    cv2.imshow("masked", image)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return 20

def cataract(sample, cx,cy):
    image = imutils.resize(sample, width=640, height=480)
    image = cv2.medianBlur(image,5)
    image = cv2.bilateralFilter(image,5,1000,1000)
   # image = image[c] TODO
    frame = image.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([20,50,120]) #all shades of yellow
    upper_red = np.array([60,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask = mask)
    image = res.copy()
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    y, x = res.shape[:2]
    total = 0
    mat = 0
    for i in range(x):
        for j in range(y):
            arr = res[j, i]
            if arr == 0:
                continue
            mat+=1
            total+=arr

    average = float(total)/float(mat)
    average = 1- np.interp(average, [0,255], [0,1])
    cv2.imshow("gray", res)
    cv2.imshow("masked", image)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return 20

def bilirubin_(request):
    sample_frame,cx,cy = camera()

    bilirubin_level = bilirubin(sample_frame,cx,cy)

    return HttpResponse('bilirubin')

def cataract_(request):
    sample_frame,cx,cy = camera()

    cataract_level = cataract(sample_frame,cx,cy)

    return HttpResponse('catarct')

def cholesterol_(request):
    sample_frame,cx,cy = camera()

    cholesterol_level = cholesterol(sample_frame,cx,cy)

    return HttpResponse("cholesterol")

