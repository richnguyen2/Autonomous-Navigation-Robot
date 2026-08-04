import numpy as np
import cv2

MIN_MATCH_COUNT = 10
img1 = cv2.imread('separatorFunnel.jpg', cv2.IMREAD_GRAYSCALE) # Template Image
img2 = cv2.imread('firstFrame.jpg', cv2.IMREAD_GRAYSCALE) # Frame

# Initiate SIFT detector
sift = cv2.SIFT_create()
orb = cv2.ORB_create(nfeatures=2000)
#surf = cv2.xfeatures2d.SURF_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
# Find 2 best matches for ratio test (instance matching)
matches = bf.knnMatch(des1,des2, k=2)

# Smaller ratio = better match, keep the m keypoints
good = []
for m,n in matches:
    if m.distance < 0.8 * n.distance:
        good.append(m)


# Amount of keypoint matches found > MIN_MATCH_COUNT
if len(good)> MIN_MATCH_COUNT:
    src_pts_list = []
    dst_pts_list = []

    for m in good:
        templateIdx = m.queryIdx
        frameIdx = m.trainIdx
        ptSrc = kp1[templateIdx].pt
        ptDst = kp2[frameIdx].pt
        src_pts_list.append(ptSrc)
        dst_pts_list.append(ptDst)
    
    # get (x,y) coordinates of the keypoints in the template and frame
    src_pts = np.float32(src_pts_list).reshape(-1, 1, 2)
    dst_pts = np.float32(dst_pts_list).reshape(-1, 1, 2)

    # Find best transformation match using RANSAC algorithm
    # M = 3x3 perspective transformation matrix, mask = inliers and outliers of the keypoint matches
    #src_dst * M -> dst_pts
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    # Map the template corners
    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

    # Only apply transformation matrix on corners to get bounding box
    dst = cv2.perspectiveTransform(pts,M)
    
    # Draws the true projected shape on the template (includes, rotation, scaling, perspective, etc.)
    img3 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2)

    img4 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    img4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)

    img5 = np.hstack((img3, img4))
    cv2.imshow("final", img5)
    cv2.waitKey(0)

else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2)

    img4 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    
    cv2.imshow("output2", img4)
    cv2.waitKey(0)