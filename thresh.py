# -*- coding:utf-8 -*-

import sys
import cv2 as cv
import numpy as np
import os
from datetime import datetime

# filename = "coi_outdoor3.pgm"
filename = sys.argv[1]

if "__main__" == __name__:
    print("Hello world!")
    print("start: ", datetime.now(), filename)
    img = cv.imread(filename)
    img = img[:, :, 0]
    img_unknown = np.copy(img)
    print(img.shape)
    print(img[400, 400])

    img_unknown[img_unknown != 255] = 0
    img_unknown[img_unknown  == 255] = 127

    # for val in np.nditer(img_unknown, op_flags=['readwrite']):
    #     if 255 == val:
    #         val[...] = 127
    #     else:
    #         val[...] = 0

    img = cv.Canny(img, 30, 80)
    img += img_unknown
    # img = cv.Laplacian(img, cv.CV_64F)
    img = 255 - img
    c = 0
    # for val in np.nditer(img, op_flags=['readwrite']):
    #   if 200 > val:
    #     val[...] = 0
    #   if 255 == val:
    #     val[...] = 127
    # c += 1
    print("c:", c)

    cv.imwrite(str(filename.split(".")[0]) + "_thresh.pgm", img)
    cv.imshow("image", img)
    while cv.waitKey(33) != 27:
        pass

