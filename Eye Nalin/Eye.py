# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import time
import math as ma

def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords

def shape_to_nps(shape):
    coords = np.zeros((shape.num_parts, 1), dtype=float)
    coords1 = np.zeros((shape.num_parts, 1), dtype=float)
    for i in range(0, shape.num_parts):
        coords[i] = shape.part(i).x
        coords1[i] = shape.part(i).y
    return coords,coords1
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMES = 1

# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
print(lStart,lEnd)
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
print(rStart, rEnd)

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

value = []

t = time.time()

while True:
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process
        #if True and not vs.more():
            #break

        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            shape = predictor(gray, rect)
            s,s1 = shape_to_nps(shape)
            s = s[36:42]
            s1 = s1[36:42]

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
