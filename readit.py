#!/usr/bin/env python

from bs4 import BeautifulSoup
import numpy as np
import re
import cv2
#https://stackoverflow.com/questions/51434091/python-globbing-a-directory-of-images

def get_distortions(data):
	Bs_data = BeautifulSoup(data, "xml")
	c_unique = Bs_data.find_all('camera_matrix')[0].data.string
	b_unique = Bs_data.find_all('distortion_coefficients')[0].data.string
	c_unique = re.sub("\s\s+" , " ", c_unique).strip()
	b_unique = re.sub("\s\s+" , " ", b_unique).strip()
	c_unique = [float(x) for x in c_unique.split(" ")]
	b_unique = [float(x) for x in b_unique.split(" ")]
	cameraMatrix = np.array(c_unique).reshape((3, 3))
	distCoeffs = np.array(b_unique)
	return cameraMatrix, distCoeffs

with open('intrinsics.xml', 'r') as f:
	data = f.read()

cameraMatrix, distCoeffs = get_distortions(data)
image_name = 'sample'
imageext = '.png'
image_dist = cv2.imread(image_name + imageext)
h, w = image_dist.shape[:2]
cameraMatrixNew, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w, h), 1, (w, h))
map1, map2 = cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, None, cameraMatrixNew, (w, h), cv2.CV_32FC1)
image_undist = cv2.remap(image_dist, map1, map2, cv2.INTER_LINEAR)

cv2.imwrite(image_name + "-improved" + imageext, image_undist)
