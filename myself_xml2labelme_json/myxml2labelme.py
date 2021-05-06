# -*- coding:utf-8 -*-
import argparse
import json
import os
import os.path as osp
import warnings
import copy
 
import numpy as np
import PIL.Image
from skimage import io
import yaml
import cv2
import copy
import re
import xml.etree.ElementTree as ET


## 自定义子函数
def mkdir_os(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars

def contain_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        return 0
    if length > 0 and len(vars) != length:
        return 0
    if length == 1:
        return 1

def get(root, name):
    vars = root.findall(name)
    return vars

## 常量定义
categories={}

## 转换函数
def convert(path):
    tree = ET.parse(path)
    root = tree.getroot()
    ## 地址文件名
    path = os.path.splitext(path)[0]
    raw_name =  os.path.basename(path) 
    imagePath = os.path.splitext(raw_name)[0]+'.png' 
    jsonname= os.path.splitext(raw_name)[0]+'.json' 

    size = get_and_check(root, 'size', 1)
    # 图片的基本信息
    width = int(float(get_and_check(size, 'width', 1).text))
    height = int(float(get_and_check(size, 'height', 1).text))

    shape_store=[]
    # try:
    for obj in get(root, 'object'):
        # 取出检测框类别名称
        category = get_and_check(obj, 'name', 1).text
        # 更新类别ID字典，判断文字是否匹配忽略大小写
        category = category.upper()
        if category not in categories:
            new_id = len(categories)
            categories[category] = new_id
        points_store=[]
        annotation = dict()
        if(contain_and_check(obj, 'points', 1)):
            for ppoints in get(obj, 'points'):
                for pointp in get(ppoints, 'point'):
                    xmin = float(get_and_check(pointp, 'x', 1).text)
                    ymin = float(get_and_check(pointp, 'y', 1).text)
                    points_store.append([xmin,ymin])

            annotation["points"]= points_store
            annotation["label"]= category
            annotation["group_id"]= 0
            annotation["shape_type"]= "polygon"
            annotation["flags"]= {}
            shape_store.append(annotation)
    #print(shape_store)


    json_dict = {
                  "version": "4.5.6",
                  "flags": {},
                  "shapes": [],
                  "imagePath": imagePath,
                  "imageData":  None,
                  "imageHeight": 600,
                  "imageWidth": 600
                }
    json_dict['shapes']= shape_store
    json_dict['imageHeight'] = height
    json_dict['imageWidth']  = width

    jsonData = json.dumps(json_dict, indent=4)
    json_path='./save_json/'
    fileObject = open(os.path.join(json_path,jsonname), 'w')
    fileObject.write(jsonData)
    fileObject.close()
    # except:
        # print("dirty~ count:")


## 启动转换
path = "./row_xml/myxml.xml"
convert(path)


## 写入类别ID字典
caaaaa={'categories':[]}
for cate, cid in categories.items():
    cat = {'supercategory': 'none', 'id': cid, 'name': cate}
    caaaaa['categories'].append(cat)
# 导出到json
json_fp = open('save_categories.txt', 'w')
json_str = json.dumps(caaaaa)
json_fp.write(json_str)
json_fp.close()

