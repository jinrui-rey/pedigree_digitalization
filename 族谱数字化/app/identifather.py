#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 18:41:32 2022

@author: zhangjinrui
"""

import img_pretreat
import pytesseract
import cv2
import pdf_pretreat
from PIL import Image


def detect_father(name, names):

    """
    用于检测 name 区域在所有姓名区域内的父亲区域
    输入需检测的姓名区域name
    输出其父亲区域的坐标
    """
    x1, y1, x2, y2 = name
    cent_name_x = (x1 + x2) / 2
    cent_name_y = (y1 + y2) / 2
    eligible_names = []
    for i in names:
        u1, v1, u2, v2 = i
        cent_x = (u1 + u2) / 2
        cent_y = (v1 + v2) / 2
        if abs(cent_y - cent_name_y) <= 10 and cent_x < cent_name_x:
            eligible_names.append(i)
        else:
            continue
    if len(eligible_names) > 0:

        elg_dict = {}
        for j in eligible_names:
            u1, v1, u2, v2 = j
            elg_cent_x = (u1 + u2) / 2
            elg_dict[elg_cent_x] = j

        father = elg_dict.get(max(elg_dict.keys()))
    else:
        father = []
    return list(father)


def detect_bro(name, names):
    """
       用于检测 name 区域在所有姓名区域内的兄弟区域
       输入需检测的姓名区域name
       输出其兄弟区域的坐标
       """
    x1, y1, x2, y2 = name
    cent_name_x = (x1 + x2) / 2
    cent_name_y = (y1 + y2) / 2
    eligible_names = []
    for i in names:
        u1, v1, u2, v2 = i
        cent_x = (u1 + u2) / 2
        cent_y = (v1 + v2) / 2
        if abs(cent_x - cent_name_x) <= 130 and 0 < cent_name_y - cent_y:
            eligible_names.append(i)
        else:
            continue
    if len(eligible_names) > 0:
        elg_dict = {}
        for j in eligible_names:
            u1, v1, u2, v2 = j
            elg_cent_y = (v1 + v2) / 2
            elg_dict[elg_cent_y] = j

        bro = elg_dict.get(max(elg_dict.keys()))
    else:
        bro = []
    # if len(eligible_names)> 0:
    #     bro = eligible_names[-1]
    # else:
    #     bro =[]
    return list(bro)


def relation_integration_dict(names):
    """
    统筹整合人物关系，输入所有姓名区域，得到一个人物关系字典

    输出字典的格式：
    key：目标姓名区域坐标
    value：目标姓名区域的父亲区域坐标

    """
    relation = {}
    for i in range(len(names)):
        x1, y1, x2, y2 = names[i]
        cent_x = (x1 + x2) / 2
        father = detect_father(names[i], names)
        if cent_x <= 320:
            relation[tuple(names[i])] = 'root'
            continue
        if len(father) == 0:  # 没有检测到父亲
            bro = detect_bro(names[i], names)

            if len(bro) != 0:
                father = detect_father(bro, names)
                while (len(father) == 0):
                    bro = detect_bro(bro, names)
                    father = detect_father(bro, names)
                relation[tuple(names[i])] = father
            else:
                relation[tuple(names[i])] = 'root'
        else:  # 检测到父亲
            relation[tuple(names[i])] = father

    return relation


def relation_integration(names):

    """
    统筹整合人物关系，输入所有姓名区域，输出一个人物关系列表

    输出列表的格式：

    relation[1] = [ ( (目标区域坐标), (目标区域的父亲区域坐标) ) ]

    """
    relation = []
    for i in range(len(names)):
        x1, y1, x2, y2 = names[i]
        cent_x = (x1 + x2) / 2
        father = detect_father(names[i], names)
        if cent_x <= 320:
            rela = (tuple(names[i]), 'root')
            relation.append(rela)
            continue
        if len(father) == 0:  # 没有检测到父亲
            bro = detect_bro(names[i], names)
            if len(bro) != 0:
                father = detect_father(bro, names)
                while (len(father) == 0):
                    bro = detect_bro(bro, names)
                    father = detect_father(bro, names)
                rela = (tuple(names[i]), tuple(father))
                relation.append(rela)
            else:
                rela = (tuple(names[i]), 'root')
                relation.append(rela)
        else:  # 检测到父亲
            rela = (tuple(names[i]), tuple(father))
            relation.append(rela)

    return relation


