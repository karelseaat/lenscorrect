#!/usr/bin/env python

import cv2
import numpy as np
import glob

# setup termination criteria for cornerSubPix()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# create and populate object points for 8x8 chessboard
objp = np.zeros((7 * 7, 3), np.float32)
objp[:,:2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

# create arrays for object points and image points
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

# gather filenames of images in folder
images = glob.glob('nogeenchecker.png')

# loop over images in folder and create chessboard corners
for fname in images:
    print(fname)
    image = cv2.imread(fname)
    gray = cv2.split(image)[0]

    ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

    if ret == True:
        objpoints.append(objp)
        corners_SubPix = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners_SubPix)
        print("Return value: ", ret)
        img = cv2.drawChessboardCorners(gray, (7, 7), corners_SubPix, ret)
        cv2.imshow("Corners", img)
        cv2.waitKey(5000)
cv2.destroyAllWindows()

# calibrate camera: cameraMatrix = 3x3 camera intrinsics matrix; distCoeffs = 5x1 vector
# gray.shape[::-1] swaps single channel image values from h, w to w, h (numpy to OpenCV format)
retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# persist intrinsics and distortions
fs = cv2.FileStorage("intrinsics.xml", cv2.FileStorage_WRITE)
fs.write("image_width", gray.shape[1])
fs.write("image_height", gray.shape[0])
fs.write("camera_matrix", cameraMatrix)
fs.write("distortion_coefficients", distCoeffs)
fs.release()
