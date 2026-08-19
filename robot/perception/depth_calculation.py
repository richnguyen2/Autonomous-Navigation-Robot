import cv2
import numpy as np
import pickle
from feature_detection import box_measure_sift

def stereo_vision_depth_calculation(image_left, image_right, camera_baseline, landmark, tolerance = 1e-6):
    left_frame = cv2.cvtColor(image_left, cv2.COLOR_BGR2GRAY)
    right_frame = cv2.cvtColor(image_right, cv2.COLOR_BGR2GRAY)

    centroids1 = box_measure_sift(left_frame, landmark)
    centroids2 = box_measure_sift(right_frame, landmark)

    if centroids1 != None and centroids2 != None:
        u_l = centroids1[0] # X value only (disparity in horizontal)
        u_r = centroids2[0]

        disparity = abs(u_l - u_r)
        if disparity < tolerance:
            depth = None
        else:
            depth = focal_length * (camera_baseline/disparity)
            depth = depth / 304.8 # Convert to ft
        
        print(str(depth) + " ft")
        return depth
    else:
        print("Depth Calc Failed")
        return None

if __name__ == "__main__":

    with open("stereo_calib.pkl", "rb") as f:
        calib = pickle.load(f)

        baseline = calib["baseline"]
        focal_length = calib["focal_length"]
        map1_L = calib["map1_L"]
        map2_L = calib["map2_L"]
        map1_R = calib["map1_R"]
        map2_R = calib["map2_R"]

    left_frame = cv2.imread("waterbottleleft0.png")
    right_frame = cv2.imread("waterbottleright0.png")
    rectified_L = cv2.remap(left_frame, map1_L, map2_L, cv2.INTER_LINEAR)
    rectified_R = cv2.remap(right_frame, map1_R, map2_R, cv2.INTER_LINEAR)
    landmark = cv2.imread("waterlandmark.png", cv2.IMREAD_GRAYSCALE)
    #cv2.imshow("img0", left_frame)
    #cv2.imshow("img1", right_frame)
    #cv2.imshow("land", landmark)
    #print("grayFrame:", right_frame.shape)
    #print("template:", landmark.shape)
    #cv2.waitKey(0)
    stereo_vision_depth_calculation(rectified_L, rectified_R, baseline, landmark)