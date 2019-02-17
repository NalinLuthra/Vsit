import sys

def do_something(val):
    EYE_AR_THRESH = 0.2
    EYE_AR_CONSEC_FRAMES = 1

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    print(lStart, lEnd)
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    print(rStart, rEnd)

    # print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Dat file doing")
    predictor = dlib.shape_predictor(os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat'))
    print("Dat file done")
    t = time.time()
    # try:
    #     vs = VideoStream(src=1).start()
    # except:
    #     vs = VideoStream(src=0).start()
    value = []

    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    print("Video started")

    while True:
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process
        # if True and not vs.more():
        # break

        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)

        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("Up till here")

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            shape = predictor(gray, rect)
            s, s1 = shape_to_nps(shape)
            s = s[36:42]
            s1 = s1[36:42]
        try:
            x = circle_eq(s, s1)
            y = circle_eq_d(s, s1)
        except:
            continue
        # print(x)
        try:
            cv2.circle(frame, (-int(x[0] / 2), -int(x[1] / 2)),
                       int(ma.sqrt((x[0] / 2) * (x[0] / 2) + (x[1] / 2) * (x[1] / 2) - x[2])), (0, 0, 255), 1)
            cv2.circle(frame, (-int(y[0] / 2), -int(y[1] / 2)),
                       int(ma.sqrt((y[0] / 2) * (y[0] / 2) + (y[1] / 2) * (y[1] / 2) - y[2])), (0, 0, 255), 1)
            x1 = x[0] / 2
            y1 = x[1] / 2
            x2 = y[0] / 2
            y2 = y[1] / 2
            distance = ma.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
            cv2.line(frame, (-x1, -y1), (-x2, -y2), (225, 0, 0), 1)  # print(-int(area))
        except OverflowError:
            continue

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    print("About to start")
    cv2.destroyAllWindows()
    vs.stop()
    print("Function done")

if __name__ == '__main__':

    do_something()