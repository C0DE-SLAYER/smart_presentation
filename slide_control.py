def slide_control(file_path):

    convert_pptx_to_jpg(file_path)

    from cvzone.HandTrackingModule import HandDetector
    from cv2 import VideoCapture, flip, imread, resize, line, FILLED, circle, imshow, waitKey, destroyAllWindows
    from os import path, listdir
    from numpy import interp

    # Parameters
    width, height = 640, 480
    gestureThreshold = 300
    folderPath = "slides"

    # Camera Setup
    # cap = VideoCapture('http://192.168.0.102:4747/video')
    cap = VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    # Hand Detector
    detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

    # Variables
    imgList = []
    delay = 30
    buttonPressed = False
    counter = 0
    drawMode = False
    imgNumber = 0
    delayCounter = 0
    annotations = [[]]
    annotationNumber = -1
    annotationStart = False
    hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

    # Get list of presentation images
    pathImages = sorted(listdir(folderPath), key=len)

    while True:
        # Get image frame
        success, img = cap.read()
        img = flip(img, 1)
        pathFullImage = path.join(folderPath, pathImages[imgNumber])
        imgCurrent = imread(pathFullImage)
        imgCurrent = resize(imgCurrent, (width, height))

        # Find the hand and its landmarks
        hands, img = detectorHand.findHands(img)  # with draw
        # Draw Gesture Threshold line
        line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

        if hands and buttonPressed is False:  # If hand is detected

            hand = hands[0]
            cx, cy = hand["center"]
            lmList = hand["lmList"]  # List of 21 Landmark points
            fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

            # Constrain values for easier drawing
            xVal = int(interp(lmList[8][0], [width // 2, width], [0, width]))
            yVal = int(interp(lmList[8][1], [150, height-150], [0, height]))
            indexFinger = xVal, yVal

            if cy <= gestureThreshold:  # If hand is at the height of the face
                if fingers == [1, 0, 0, 0, 0]:
                    print("Left")
                    buttonPressed = True
                    if imgNumber > 0:
                        imgNumber -= 1
                        annotations = [[]]
                        annotationNumber = -1
                        annotationStart = False
                if fingers == [0, 0, 0, 0, 1]:
                    print("Right")
                    buttonPressed = True
                    if imgNumber < len(pathImages) - 1:
                        imgNumber += 1
                        annotations = [[]]
                        annotationNumber = -1
                        annotationStart = False

            if fingers == [0, 1, 1, 0, 0]:
                circle(imgCurrent, indexFinger, 12, (0, 0, 255), FILLED)

            if fingers == [0, 1, 0, 0, 0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                print(annotationNumber)
                annotations[annotationNumber].append(indexFinger)
                circle(imgCurrent, indexFinger, 12, (0, 0, 255), FILLED)

            else:
                annotationStart = False

            if fingers == [0, 1, 1, 1, 0]:
                if annotations:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True

        else:
            annotationStart = False

        if buttonPressed:
            counter += 1
            if counter > delay:
                counter = 0
                buttonPressed = False

        for i, annotation in enumerate(annotations):
            for j in range(len(annotation)):
                if j != 0:
                    line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

        imgSmall = resize(img, (ws, hs))
        h, w, _ = imgCurrent.shape
        imgCurrent[0:hs, w - ws: w] = imgSmall

        imshow("Slides", imgCurrent)
        imshow("Image", img)

        key = waitKey(1)
        if key == ord('q'):
            break

    destroyAllWindows()

    return False


def convert_pptx_to_jpg(file_path):
    import convertapi
    from os import getenv, mkdir, remove
    from pdf2image import convert_from_path
    from dotenv import load_dotenv

    load_dotenv()

    convertapi.api_secret = getenv('CONVERTAPI_API_SECRET')

    result = convertapi.convert('pdf', {'File': file_path})
    result.save_files('results.pdf')

    try:
        mkdir('slides')
    except:
        print('dir exists')

    images = convert_from_path('results.pdf', dpi=200) 

    for i, image in enumerate(images, start=1):
        image.save(f'slides/{i}.jpg', "JPEG")  
    
    remove('results.pdf')
