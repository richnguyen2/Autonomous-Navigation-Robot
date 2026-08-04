import cv2
import time
import numpy as np

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

# Reduce matches with ratio test and apply transformation
def imageTransformation(matches, kp1, kp2, template):
    MIN_MATCH_COUNT = 10
    # Smaller ratio = better match, filter keypoints
    good = []
    for m,n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)

    # Amount of keypoint matches found > MIN_MATCH_COUNT
    if len(good)> MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

        # Map the template corners
        h,w = template.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

        # Apply transformation matrix on corners and normalize to get bounding box
        # Output are the frame coords of the 4 corners
        dst = cv2.perspectiveTransform(pts,M)

    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        dst = None
    
    return dst

def templateMatch(grayFrame, template, method = cv2.TM_CCOEFF_NORMED):
    h, w = template.shape
    res = cv2.matchTemplate(grayFrame, template, method)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    topLeft = maxLoc
    botRight = (topLeft[0] + w, topLeft[1] + h)
    return topLeft, botRight, maxVal

def siftMatch(grayFrame, template):
    MIN_MATCH_COUNT = 10
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(template, None) # template
    kp2, des2 = sift.detectAndCompute(grayFrame, None) # frame

    # Match descriptors.
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(des1,des2, k=2)

    dst = imageTransformation(matches, kp1, kp2, template)
    
    return dst

def orbMatch(grayFrame, template):
    dst = None
    orb = cv2.ORB_create(
        nfeatures=2000,
        fastThreshold=10,
        nlevels=12)
    kp1, des1 = orb.detectAndCompute(template,None) # template
    kp2, des2 = orb.detectAndCompute(grayFrame,None) # frame

    # Match descriptors.
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)

    dst = imageTransformation(matches, kp1, kp2, template)

    return dst

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

    # SIFT Matching
    dst = siftMatch(grayFrame, sepFunnelTemplate)
    print(dst)
    # Draw bounding box if match is found
    if dst is not None:
        cv2.polylines(frame_resized,[np.int32(dst)],True, blue, lineW, cv2.LINE_AA)

    # Save frame to video recording
    out.write(frame_resized)
    cv2.imshow('Video', frame_resized)

    # FPS Calculation
    dt = time.time() - lastT
    currFPS = 1/dt
    FPSFilter = FPSFilter * .9 + currFPS * .1
    lastT = time.time()
    #print("FPS: ", FPSFilter)

    if cv2.waitKey(1) & 0xff == ord('q'):
       break

out.release()
myVid.release()
cv2.destroyAllWindows()