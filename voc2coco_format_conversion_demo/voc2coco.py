# -*- coding=utf-8 -*-
#!/usr/bin/python

import sys
import os
import shutil
import numpy as np
import json
import xml.etree.ElementTree as ET



# 检测框的ID起始值
START_BOUNDING_BOX_ID = 1
# 类别列表无必要预先创建，程序中会根据所有图像中包含的ID来创建并更新
PRE_DEFINE_CATEGORIES = {}
# If necessary, pre-define category and its id
#  PRE_DEFINE_CATEGORIES = {"aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4,
                         #  "bottle":5, "bus": 6, "car": 7, "cat": 8, "chair": 9,
                         #  "cow": 10, "diningtable": 11, "dog": 12, "horse": 13,
                         #  "motorbike": 14, "person": 15, "pottedplant": 16,
                         #  "sheep": 17, "sofa": 18, "train": 19, "tvmonitor": 20}


def get(root, name):
    vars = root.findall(name)
    return vars


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
    


# 得到图片唯一标识号
def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        return int(filename)
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.'%(filename))

# import argparse
# import json
# import matplotlib.pyplot as plt
# import skimage.io as io
# import cv2
# from labelme import utils
# import numpy as np
# import glob
# import PIL.Image
# from shapely.geometry import Polygon #https://shapely.readthedocs.io/en/latest/manual.html#geometric-objects

# def polygons_to_mask(img_shape, polygons):
        # mask = np.zeros(img_shape, dtype=np.uint8)
        # mask = PIL.Image.fromarray(mask)
        # xy = list(map(tuple, polygons))
        # PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        # mask = np.array(mask, dtype=bool)
        # return mask
        
# def getbbox(points,height,width):
        # # img = np.zeros([self.height,self.width],np.uint8)
        # # cv2.polylines(img, [np.asarray(points)], True, 1, lineType=cv2.LINE_AA)  # 画边界线
        # # cv2.fillPoly(img, [np.asarray(points)], 1)  # 画多边形 内部像素值为1
        # polygons = points
        # mask = polygons_to_mask([height,width], polygons)

        # '''从mask反算出其边框
        # mask：[h,w]  0、1组成的图片
        # 1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        # '''
        # # np.where(mask==1)
        # index = np.argwhere(mask == 1)
        # rows = index[:, 0]
        # clos = index[:, 1]
        # # 解析左上角行列号
        # left_top_r = np.min(rows)  # y
        # left_top_c = np.min(clos)  # x

        # # 解析右下角行列号
        # right_bottom_r = np.max(rows)
        # right_bottom_c = np.max(clos)
        # return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

import re
def convert(xml_list, xml_dir, json_file):
    '''
    :param xml_list: 需要转换的XML文件列表
    :param xml_dir: XML的存储文件夹
    :param json_file: 导出json文件的路径
    :return: None
    '''
    list_fp = xml_list
    # 标注基本结构
    json_dict = {"images":[],
                 "type": "instances",
                 "annotations": [],
                 "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    indexiiii=0
    # 坏的标注
    dirtySample=0

    for line in list_fp:
        line = line.strip()
        #print("buddy~ Processing {}".format(line))
        # 解析XML
        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        path = get(root, 'path')
        
        # # 取出图片名字
        # if len(path) == 1:
            # filename = os.path.basename(path[0].text)
        # elif len(path) == 0:
            # filename = get_and_check(root, 'filename', 1).text
        # else:
            # raise NotImplementedError('%d paths found in %s'%(len(path), line))
            
        filename = os.path.splitext(line)[0]+'.png'
        ## The filename must be a number
        indexiiii=indexiiii+1
        image_id = indexiiii  # 图片ID
        size = get_and_check(root, 'size', 1)
        # 图片的基本信息
        width = int(float(get_and_check(size, 'width', 1).text))
        height = int(float(get_and_check(size, 'height', 1).text))

        ## Cruuently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        # 处理每个标注的检测框
        try:
            for obj in get(root, 'object'):
                # 取出检测框类别名称
                category = get_and_check(obj, 'name', 1).text
                # 更新类别ID字典，判断文字是否匹配忽略大小写
                category = category.upper()
                if category not in categories:
                    new_id = len(categories)
                    categories[category] = new_id
                category_id = categories[category]

                if(contain_and_check(obj, 'bndbox', 1)):
                    bndbox = get_and_check(obj, 'bndbox', 1)
                    xmin = int(float(get_and_check(bndbox, 'xmin', 1).text)) - 1
                    ymin = int(float(get_and_check(bndbox, 'ymin', 1).text)) - 1
                    xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
                    ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))
                    assert(xmax > xmin)
                    assert(ymax > ymin)
                    o_width = abs(xmax - xmin)
                    o_height = abs(ymax - ymin)
                    annotation = dict()
                    annotation['area'] = o_width*o_height
                    annotation['iscrowd'] = 0
                    annotation['image_id'] = image_id
                    annotation['bbox'] = [xmin, ymin, o_width, o_height]
                    annotation['category_id'] = category_id
                    annotation['id'] = bnd_id
                    annotation['ignore'] = 0
                    # 设置分割数据，点的顺序为逆时针方向
                    annotation['segmentation'] = [[xmin,ymin,xmin,ymax,xmax,ymax,xmax,ymin]]

                    json_dict['annotations'].append(annotation)
                    bnd_id = bnd_id + 1
                else:
                    for ppoints in get(obj, 'points'):
                        for pointp in get(ppoints, 'point'):
                            xmin = int(float(get_and_check(pointp, 'x', 1).text))- 1
                            ymin = int(float(get_and_check(pointp, 'y', 1).text)) - 1
                            xmax = int(float(get_and_check(pointp, 'x', 1).text))+10
                            ymax = int(float(get_and_check(pointp, 'y', 1).text))+10
                            assert(xmax > xmin)
                            assert(ymax > ymin)
                            o_width = abs(xmax - xmin)
                            o_height = abs(ymax - ymin)
                            annotation = dict()
                            annotation['area'] = o_width*o_height
                            annotation['iscrowd'] = 0
                            annotation['image_id'] = image_id
                            annotation['bbox'] = [xmin, ymin, o_width, o_height]
                            annotation['category_id'] = category_id
                            annotation['id'] = bnd_id
                            annotation['ignore'] = 0
                            # 设置分割数据，点的顺序为逆时针方向
                            annotation['segmentation'] = [[xmin,ymin,xmin,ymax,xmax,ymax,xmax,ymin]]

                            json_dict['annotations'].append(annotation)
                            bnd_id = bnd_id + 1
            image = {'file_name': filename,
                     'height': height,
                     'width': width,
                     'id':image_id}
            json_dict['images'].append(image)
        except:
            dirtySample=dirtySample+1
            print("dirty~ count: {}".format(dirtySample))
            print("dirty~ image_id: {}".format(image_id))

    # 写入类别ID字典
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    # 导出到json
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()




import os, shutil
from tqdm import *

def checkJpgXml(jpeg_dir, annot_dir):
    """
    dir1 是图片所在文件夹
    dir2 是标注文件所在文件夹
    """
    pBar = tqdm(total=len(os.listdir(jpeg_dir)))
    cnt = 0
    for file in os.listdir(jpeg_dir):
        pBar.update(1)
        f_name, f_ext = file.split(".")
        if not os.path.exists(os.path.join(annot_dir, f_name + ".xml")):
            print(f_name)
            cnt += 1

    if cnt > 0:
        print("有%d个文件不符合要求。" % (cnt))
    else:
        print("所有图片和对应的xml文件都是一一对应的。")


# 1. 检查jpg和xml文件是否是一一对应的
jpegimages_dir = r".\JPEGImages"  # 图片保存位置
annotations_dir = r".\Annotations"  # 标注文件保存位置
print("=" * 5, "\t1. checking jpg and xml\t", "=" * 5)
checkJpgXml(jpeg_dir=jpegimages_dir, annot_dir=annotations_dir)


if __name__ == '__main__':
    root_path = os.getcwd()
    xml_dir = os.path.join(root_path, 'Annotations')

    xml_labels = os.listdir(os.path.join(root_path, 'Annotations'))
    np.random.shuffle(xml_labels)
    split_point = int(len(xml_labels)/10)

    print("=" * 5, "\t2. val2014 jpg and xml\t", "=" * 5)
    # validation data
    xml_list = xml_labels[0:split_point]
    json_file = './instances_val2014.json'
    convert(xml_list, xml_dir, json_file)
    for xml_file in xml_list:
        img_name = xml_file[:-4] + '.png'
        shutil.copy(os.path.join(root_path, 'JPEGImages', img_name),
                    os.path.join(root_path, 'val2014', img_name))
    
    print("=" * 5, "\t2. train2014 jpg and xml\t", "=" * 5)
    # train data
    xml_list = xml_labels[split_point:]

    json_file = './instances_train2014.json'
    convert(xml_list, xml_dir, json_file)
    for xml_file in xml_list:
        img_name = xml_file[:-4] + '.png'
        shutil.copy(os.path.join(root_path, 'JPEGImages', img_name),
                    os.path.join(root_path, 'train2014', img_name))
    