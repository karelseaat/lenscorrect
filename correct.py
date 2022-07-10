#!/usr/bin/env python

import re
import glob
import cv2
import numpy as np
from bs4 import BeautifulSoup
#https://stackoverflow.com/questions/51434091/python-globbing-a-directory-of-images

def get_distortions(data):
    bs_data = BeautifulSoup(data, "xml")
    c_unique = bs_data.find_all('camera_matrix')[0].data.string
    b_unique = bs_data.find_all('distortion_coefficients')[0].data.string
    c_unique = re.sub(r"\s\s+" , " ", c_unique).strip()
    b_unique = re.sub(r"\s\s+" , " ", b_unique).strip()
    c_unique = [float(x) for x in c_unique.split(" ")]
    b_unique = [float(x) for x in b_unique.split(" ")]
    camera_matrix = np.array(c_unique).reshape((3, 3))
    dist_coeffs = np.array(b_unique)
    return camera_matrix, dist_coeffs

def correct_image(image, data):
    if "." in image:
        image_name, imageext = image.split(".")
        camera_matrix, dist_coeffs = get_distortions(data)
        image_dist = cv2.imread(image_name + '.' +imageext)
        height, width = image_dist.shape[:2]
        camera_matrix_new, _ = cv2.getOptimalNewCameraMatrix(
			camera_matrix, dist_coeffs, (width, height), 1, (width, height)
		)
        map1, map2 = cv2.initUndistortRectifyMap(
			camera_matrix, dist_coeffs, None, camera_matrix_new, (width, height), cv2.CV_32FC1
		)
        image_undist = cv2.remap(image_dist, map1, map2, cv2.INTER_LINEAR)
        cv2.imwrite(image_name + "-improved." + imageext, image_undist)

with open('intrinsics.xml', 'r') as f:
    correction_data = f.read()

    for image_name in  glob.glob("*[!improved].png"):
        correct_image(image_name, correction_data)
