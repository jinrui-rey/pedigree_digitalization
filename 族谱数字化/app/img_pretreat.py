# env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 6 18:41:32 2022

@author: rey
"""

import cv2
import os
import numpy as np
import random
import sys
import pytesseract
from PIL import Image

# 长宽比大于此值，则判定为不是完整汉字,则扩大范围
MAX_CHAR_RATIO = 1.5

# 长宽比大于此值，则判定为线
MIN_LINE_RATIO = 1.5

# 文字的半宽度
AVERATE_HALF_LENTH = 18


def NMS(boxes, overlapThresh):
    """
    boxes: boxes为一个m*n的矩阵，m为bbox的个数，n的前4列为每个bbox的坐标，
           格式为（x1,y1,x2,y2），有时会有第5列，该列为每一类的置信
    overlapThresh: 最大允许重叠率
    """
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []

    # grab the coordinates of all bounding boxes respectively
    x1 = boxes[:, 0]  # startX
    y1 = boxes[:, 1]  # startY
    x2 = boxes[:, 2]  # endX
    y2 = boxes[:, 3]  # endY
    # probs = boxes[:,4]


    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # if probabilities are provided, sort by them instead
    # idxs = np.argsort(probs)

    # keep looping while some indexes still remain in the idxs list
    while len(idxs) > 0:

        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # the ratio of overlap in the bounding box
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that overlap is larger than overlapThresh
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")


def random_color(): # 画出外边线框，但会影响OCR识别
    def random_num():
        return random.randint(0, 255)

    return 255, 255, 255


def draw_rectangle(image, region, color):
    cv2.rectangle(image, (region[0], region[1]), (region[2], region[3]),
                  color, 2)


def horizontal_projection(binary_image: np.array, trim: bool = False) -> np.array:  # 水平投影
    result = np.zeros_like(binary_image)
    min_count = binary_image.shape[1]
    for i, row in enumerate(binary_image):
        nonzero_count = row[row != 0].size
        result[i, -nonzero_count:] = 255
        min_count = min(min_count, nonzero_count)
    if trim:
        result = result[:, :-min_count]
    return result


def vertical_projection(binary_image: np.array, trim: bool = False) -> np.array:    # 竖直投影
    result = np.zeros_like(binary_image)
    min_count = binary_image.shape[0]
    for i in range(binary_image.shape[1]):
        column = binary_image[:, i]
        nonzero_count = column[column != 0].size
        result[-nonzero_count:, i] = 255
        min_count = min(min_count, nonzero_count)
    if trim:
        result = result[:-min_count, :]
    return result


def merge_part(coordinate): # 融合偏旁部首等远离文字等部分
    for i in range(len(coordinate)):
        for j in range(len(coordinate)):
            if i != j:
                x1, y1, x2, y2 = coordinate[i]
                cent1_x = (x1 + x2) / 2
                cent1_y = (y1 + y2) / 2
                u1, v1, u2, v2 = coordinate[j]
                cent2_x = (u1 + u2) / 2
                cent2_y = (v1 + v2) / 2

                cent_dist = max(abs(cent1_x - cent2_x) / 2, abs(cent2_y - cent1_y) / 2)

                if cent_dist < AVERATE_HALF_LENTH:
                    coordinate[j] = [min(x1, u1), min(y1, v1), max(u2, x2), max(v2, y2)]


def merge_name(coordinate): # 融合单个文字为姓名
    for i in range(len(coordinate)):
        for j in range(len(coordinate)):
            if i != j:
                x1, y1, x2, y2 = coordinate[i]
                u1, v1, u2, v2 = coordinate[j]

                cent1_x = (x1 + x2) / 2
                cent1_y = (y1 + y2) / 2
                cent2_x = (u1 + u2) / 2
                cent2_y = (v1 + v2) / 2

                cent_dist = abs(cent1_x - cent2_x) / 2

                cent_dist = max(abs(cent1_x - cent2_x) / 2, abs(cent2_y - cent1_y) / 2)

                if cent_dist < 2.2 * AVERATE_HALF_LENTH:
                    coordinate[j] = [min(x1, u1), min(y1, v1), max(u2, x2), max(v2, y2)]


def reject_line(coordinate):    # 剔除吊线
    for i in range(len(coordinate)):
        x1, y1, x2, y2 = coordinate[i]
        side_x = abs(x2 - x1)
        side_y = abs(y2 - y1)
        large_side = side_x if side_x > side_y else side_y
        small_side = side_x if side_x < side_y else side_y

        if large_side == 0 or small_side == 0:
            continue
        ratio = large_side / small_side

        if ratio > MAX_CHAR_RATIO:
            coordinate[i] = [0, 0, 0, 0]


def reject_small_regions(coordinate):   # 剔除过小的非文字区域
    for i in range(len(coordinate)):
        x1, y1, x2, y2 = coordinate[i]
        side_x = abs(x2 - x1)
        side_y = abs(y2 - y1)

        area = side_x * side_y

        if area < 2400:  # 估计值，需要随时改变
            coordinate[i] = [0, 0, 0, 0]


def cut_title(bimg, img):   # 去除标题
    _ = list(np.count_nonzero(bimg, axis=1))
    black = [bimg.shape[1] - i for i in _]
    result = img[black.index(max(black)) + 5:, :]
    return result


def vertical_cut(vt, img):  # 左右拼接
    _ = list(np.count_nonzero(vt, axis=0))

    black = [vt.shape[0] - i for i in _]

    l = img[:, :round(0.5 * vt.shape[1])]
    r = img[:, round(0.5 * vt.shape[1]):]

    # l = img[:,:black.index(max(black))]
    # r = img[:,abs(vt.shape[1] - black.index(max(black))):]

    img_list = [l, r]
    result = np.concatenate(img_list, axis=0)
    return result


def horizontal_cut(hr, img):  # 去除世代标识
    _ = list(np.count_nonzero(hr, axis=1))
    black_value = [hr.shape[1] - i for i in _]
    queue = []
    delete_zone = []
    criteria = 900

    for i in range(len(black_value)):
        if black_value[i] > criteria:
            queue.append(i)
            if len(queue) > 8:
                delete_zone.append(min(queue))
                queue.clear()
            # if len(queue) < 8 and black_value[i] <= criteria:
            # queue.clear()

    for i in delete_zone.copy():
        for j in range(i - 10, i + 20):
            delete_zone.append(j)

    result = np.delete(img, delete_zone, axis=0)
    result = result[80:-100, :]

    return result


def clude_name(img_path: object) -> object:
    """
    此函数为统筹各个步骤和函数，输入所需图片，输出姓名区域坐标

    """
    # img_path = sys.argv[1]
    # 原图导入
    '''
    0， 图片预处理
    '''
    img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 原图水平投影
    hp = horizontal_projection(bin_img)

    # 原图基础上裁去标题
    notitle = cut_title(hp, img)
    gray_no_title = cv2.cvtColor(notitle, cv2.COLOR_BGR2GRAY)
    _, bin_no_title = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite('out/notitle.jpg', notitle)

    # 左右切割后拼接
    vt_cut = vertical_cut(bin_no_title, notitle)
    cv2.imwrite('out/vt_cut.jpg', vt_cut)
    gray_vt_cut = cv2.cvtColor(vt_cut, cv2.COLOR_BGR2GRAY)
    _, bin_vt_cut = cv2.threshold(gray_vt_cut, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 切除黑框后的原图
    hr_cut = horizontal_cut(bin_vt_cut, vt_cut)
    cv2.imwrite('out/hr_cut.jpg', hr_cut)

    '''
    1.文件创建，得到MSER对象

    '''
    # 读预处理后的文件，拷贝出
    # 备份
    img = cv2.imread(r'out/hr_cut.jpg')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图

    pic_1 = img.copy()
    pic_2 = img.copy()

    # 得到mser对象
    mser = cv2.MSER_create(delta=5, min_area=10, max_variation=0.5)
    regions, boxes = mser.detectRegions(gray_img)

    """
    2.NMS过滤
    """
    # 无NMS过滤
    coordinate = []
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(pic_1, (x, y), (x + w, y + h), (255, 0, 0), 2)
        coordinate.append([x, y, x + w, y + h])

    # #经NMS过滤
    picks = NMS(np.array(coordinate), overlapThresh=0.5)

    """
    3.框的细部处理

    """

    # 融合小块
    merge_part(picks)
    # 剔除小块
    reject_small_regions(picks)
    # 剔除线
    reject_line(picks)
    # 剔除0坐标
    picks_zerofree = np.delete(picks, np.where(picks == [0, 0, 0, 0]), axis=0)

    # 融合名字
    merge_name(picks_zerofree)
    # 删除重复项
    picks_norepeat = np.unique(picks_zerofree, axis=0)

    for pick in picks_norepeat:
        color = random_color()
        draw_rectangle(pic_2, pick, color)

    cv2.imwrite('out/with_out_nms.jpg', pic_1)
    cv2.imwrite('out/result.jpg', pic_2)

    globals()['boxes'] = picks_norepeat

    return picks_norepeat


def winnow_names(img, boxes):
    """
    此函数用于剪裁并输出姓名区域

    """
    i = 0
    for box in boxes:
        x1, y1, x2, y2 = box
        name = img[y1:y2, x1:x2]
        cv2.imwrite('out/{}.jpg'.format(i), name)
        i = i + 1
