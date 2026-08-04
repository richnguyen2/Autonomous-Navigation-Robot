import cv2
import time

# Drawing Parameters
blue = (255, 0, 0)
red = (0, 0, 255)
lineW = 2
videoScale = 0.5
threshold = .3

# Video and Template Initialization
myVid = cv2.VideoCapture('video.mp4')
cupTemplate = cv2.imread('cup.jpg', cv2.IMREAD_GRAYSCALE)
sepFunnelTemplate = cv2.imread('separatorFunnel.jpg', cv2.IMREAD_GRAYSCALE)
fps = myVid.get(cv2.CAP_PROP_FPS)
width = int(myVid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(myVid.get(cv2.CAP_PROP_FRAME_HEIGHT))
scaledW = int(width * videoScale)
scaledH = int(height * videoScale)

# Video output parameters
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (scaledW, scaledH))

def templateMatch(grayFrame, template, method = cv2.TM_CCOEFF_NORMED):
    h, w = template.shape
    res = cv2.matchTemplate(grayFrame, template, method)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    topLeft = maxLoc
    botRight = (topLeft[0] + w, topLeft[1] + h)
    return topLeft, botRight, maxVal

def templateMatch2(grayFrame, template, method = cv2.TM_CCOEFF_NORMED):
    h, w = template.shape
    res = cv2.matchTemplate(grayFrame, template, method)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    x, y = maxLoc
    return x, y, w, h, maxVal

# Start time
lastT = time.time()
FPSFilter = 30

while myVid.isOpened():
    ret, frame = myVid.read()

    if not ret:
        print("Video Ended")
        break

    # Shrink Frame and convert to Gray scale for better performance
    frame_resized = cv2.resize(frame, None, fx=videoScale, fy=videoScale)
    grayFrame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

    # Template Matching
    topLeftCup, botRightCup, cupConf = templateMatch(grayFrame, cupTemplate)
    topLeftFunnel, botRightFunnel, funnelConf = templateMatch(grayFrame, sepFunnelTemplate)

    # Draw Bounding Boxes based on confidence threshold
    if cupConf > threshold:
        cv2.rectangle(frame_resized, topLeftCup, botRightCup, blue, lineW)
    if funnelConf > threshold:
        cv2.rectangle(frame_resized, topLeftFunnel, botRightFunnel, red, lineW)

    # Save frame to video recording
    out.write(frame_resized)
    cv2.imshow('Video', frame_resized)

    # FPS Calculation
    dt = time.time() - lastT
    currFPS = 1/dt
    FPSFilter = FPSFilter * .9 + currFPS * .1
    lastT = time.time()
    #print(FPSFilter)

    if cv2.waitKey(1) & 0xff == ord('q'):
       break

out.release()
myVid.release()
cv2.destroyAllWindows()
