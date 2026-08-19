# Script to find the landmark/object

import cv2
import numpy as np

blue = (255, 0, 0)
red = (0, 0, 255)
lineW = 2
videoScale = 0.5
threshold = .3

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

        # Get Homogenous matrix transformation between the template and actual image
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

################# Detect Object and return ROI #####################

def templateMatch(grayFrame, template, method = cv2.TM_CCOEFF_NORMED):
    h, w = template.shape
    res = cv2.matchTemplate(grayFrame, template, method)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    x, y = maxLoc
    return x, y, w, h, maxVal

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


################# Get Centroid and draw Bounding Box #####################

# Get centroid of detected object using template matching
def box_measure_template(grayFrame, template, threshold=.9):
    x, y, w, h, maxVal = templateMatch(grayFrame, template)
    print(maxVal)
    if maxVal > threshold:
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        topLeft = (x, y)
        botRight = (topLeft[0] + w, topLeft[1] + h)
        cv2.rectangle(grayFrame, topLeft, botRight, blue, lineW)
        cv2.imshow("img", grayFrame)
        cv2.waitKey(0)
        return cx, cy
    else:
        return None

# Get centroid of detected object using SIFT
def box_measure_sift(grayFrame, template):
    dst = siftMatch(grayFrame, template)
    if dst is not None:
        centroid = np.mean(dst.reshape(4,2), axis=0)
        cx = centroid[0]
        cy = centroid[1]
        cv2.polylines(grayFrame,[np.int32(dst)],True, blue, lineW, cv2.LINE_AA)
        cv2.circle(grayFrame, (int(cx), int(cy)), 8, blue, 2)
        cv2.imshow("img", grayFrame)
        cv2.waitKey(0)
        return cx, cy
    else:
        return None