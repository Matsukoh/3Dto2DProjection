# -*- coding:utf-8 -*-

import sys
import cv2 as cv
import numpy as np
import os
from datetime import datetime
from functools import partial

# filename = os.environ["HOME"]+"/Downloads/coi_1cm_ascii.pcd"
filename = sys.argv[1]
res = 0.05
size = 200.0


def getPoint(line):
    return map(float, line.rstrip().split(" "))


def getIndex(x, y):
    return int((x+size/2.0)/res), int((size/2.0-y)/res)


if "__main__" == __name__:
    print("Hello world!")
    print("start: ", datetime.now(), filename)
    # (縦,横)
    img = np.zeros((int(size/res), int(size/res), 1), dtype=np.uint8)
    img[:, :] = 255
    # (天井からの距離，左壁からの距離)
    # img[(10,5)] = [255]
    # img[10,5] = [255,255,255]
    # 表示して[ESC]が押されるまで待つ
    # img = np.zeros((2500,2500,3), dtype=np.uint8)
    print(img.dtype)

    buffer = 2 ** 16
    with open(filename, "r") as f:
        row_length = sum(x.count('\n') for x in iter(partial(f.read, buffer), ''))
        print("Row length is " + str('{:,}'.format(row_length)))

    with open(filename, "r") as pcd:
        # ヘッダーとばす
        # head = ""
        # while "DATA" != head:
        #     head = pcd.readline().rstrip().split(" ")[0]
        i = 0
        line = pcd.readline()
        while line:
            line = np.array(line.replace("\n", "").split(" ")).astype('f8')
            # print(line[3], line[4], line[5])
            if -size / 2 < line[2] < size / 2 and -size / 2 < line[3] < size / 2 and line[4] < 3.0:
                x, y = getIndex(line[2], line[3])
                if 0 < img[(y, x)]:
                    img[(y, x)] -= 1
            line = pcd.readline()
            if 0 == i % 50000:
                print("line num : " + str('{:,}'.format(i)) + "/" + str('{:,}'.format(row_length)))
                print(line)
            i += 1
    print("end converting")
    print("end: ", datetime.now(), filename)
    cv.imwrite(str(filename.split(".")[0]) + ".pgm", img)
    cv.imshow("image", img)
    while cv.waitKey(33) != 27:
        pass

