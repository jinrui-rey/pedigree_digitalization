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
    x1, y1, x2, y2 = name
    cent_name_x = (x1 + x2) / 2
    cent_name_y = (y1 + y2) / 2
    eligible_names = []
    for i in names:
        u1, v1, u2, v2 = i
        cent_x = (u1 + u2) / 2
        cent_y = (v1 + v2) / 2
        if abs(cent_y - cent_name_y) <= 50 and cent_x < cent_name_x:
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


def build_tree(names):
    for i in range(len(names)):
        x1, y1, x2, y2 = names[i]
        global gray_img
        array = gray_img[y1 - 10:y2 + 10, x1 - 10:x2 + 10]
        text = pytesseract.image_to_string(array, lang='chi_sim', config='--psm 7, --oem 1,-c max_characters_to_try=2')

        global TreeNode_list

        father = detect_father(names[i], names)
        if len(father) != 0:
            x1, y1, x2, y2 = father
            father_area = gray_img[y1 - 10:y2 + 10, x1 - 10:x2 + 10]
            father_name = pytesseract.image_to_string(father_area, lang='chi_sim',
                                                      config='--psm 7, --oem 1, -c max_characters_to_try=2')
            j = globals()['name' + str(i)] = TreeNode(text, names[i], father=father_name)
            TreeNode_list.append(j)

        else:

            bro = PdfDetect_bro(names[i], names)
            if len(bro) != 0:
                x1, y1, x2, y2 = bro
                bro_area = gray_img[y1 - 10:y2 + 10, x1 - 10:x2 + 10]
                bro_name = pytesseract.image_to_string(bro_area, lang='chi_sim',
                                                       config='--psm 7, --oem 1,-c max_characters_to_try=2')
                j = globals()['name' + str(i)] = TreeNode(text, names[i], bro=bro_name)
                TreeNode_list.append(j)

        if len(father) == 0 and len(bro) == 0:
            j = globals()['name' + str(i)] = TreeNode(text, names[i], father=0, bro=0)
            TreeNode_list.append(j)


def PdfDetect_bro(name, names):
    x1, y1, x2, y2 = name
    cent_name_x = (x1 + x2) / 2
    cent_name_y = (y1 + y2) / 2
    eligible_names = []
    for i in names:
        u1, v1, u2, v2 = i
        cent_x = (u1 + u2) / 2
        cent_y = (v1 + v2) / 2
        if abs(cent_x - cent_name_x) <= 250 and 5 < cent_name_y - cent_y:
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


def PdfRelation_integration_dict(names):
    relation = {}

    for i in range(len(names)):
        x1, y1, x2, y2 = names[i]
        cent_x = (x1 + x2) / 2
        father = detect_father(names[i], names)
        if cent_x <= 450:
            relation[tuple(names[i])] = 'root'
            continue
        if len(father) == 0:  # 没有检测到父亲
            bro = PdfDetect_bro(names[i], names)
            if len(bro) != 0:
                father = detect_father(bro, names)
                while (len(father)) == 0:
                    bro = PdfDetect_bro(bro, names)
                    father = detect_father(bro, names)
                relation[tuple(names[i])] = father
            else:
                relation[tuple(names[i])] = 'root'
        else:  # 检测到父亲
            relation[tuple(names[i])] = father

    return relation

def PdfRelation_integration_dict_backup(names):
    relation = {}

    for i in range(len(names)):
        x1, y1, x2, y2 = names[i]
        cent_x = (x1 + x2) / 2
        father = detect_father(names[i], names)
        if cent_x <= 450:
            relation[tuple(names[i])] = 'root'
            continue
        if len(father) == 0:  # 没有检测到父亲
            bro = PdfDetect_bro(names[i], names)
            if len(bro) != 0:
                father = detect_father(bro, names)
                relation[tuple(names[i])] = father
                while (len(father)) == 0:
                    bro = PdfDetect_bro(bro, names)
                    if len(bro)==0:
                        relation[tuple(names[i])] = 'root1'
                        break
                    else:
                        father = detect_father(bro, names)
                        relation[tuple(names[i])] = father
            else:
                relation[tuple(names[i])] = 'root'
        else:  # 检测到父亲
            relation[tuple(names[i])] = father

    return relation




class TreeNode:
    def __init__(self, name, coordinate, father=None, bro=None):
        self.name = name
        self.coordinate = coordinate
        self.father = father
        self.bro = bro

    def show_name(self):
        if self.father == None:
            print("{} bro is {}".format(self.name, self.bro))
        else:
            print("{} father is {}".format(self.name, self.father))

    def list_all_member(self):
        for name, value in vars(self).items():
            if self.father == None:
                print("{} bro is {}".format(self.name, self.bro))
            else:
                print("{} father is {}".format(self.name, self.father))
