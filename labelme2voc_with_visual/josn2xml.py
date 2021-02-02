import os
import glob
import json
import cv2
import codecs
import numpy as np
#标签路径
labelme_path = "./data_annotated/"              #原始labelme标注数据路径
saved_path = "./save/"                #保存路径
#获取待处理文件
files = glob.glob(labelme_path + "*.json")
files = [i.split("/")[-1].split(".json")[0] for i in files]
 
#读取标注信息并写入 xml
for json_file_ in files:
    file_dir = os.path.split(json_file_)[0]
    file_name = os.path.split(json_file_)[1]
    json_filename =  json_file_ + ".json"
    json_file = json.load(open(json_filename, "r", encoding="utf-8"))
    height, width, channels = cv2.imread( json_file_ +".jpg").shape
    with codecs.open(saved_path + json_file_ + ".xml", "w", "utf-8") as xml:
        xml.write('<annotation>\n')
        xml.write('\t<folder>' + 'DF_data' + '</folder>\n')
        xml.write('\t<filename>' + file_name + ".jpg" + '</filename>\n')
        xml.write('\t<source>\n')
        xml.write('\t\t<database>The UAV autolanding</database>\n')
        xml.write('\t\t<annotation>UAV AutoLanding</annotation>\n')
        xml.write('\t\t<image>flickr</image>\n')
        xml.write('\t\t<flickrid>NULL</flickrid>\n')
        xml.write('\t</source>\n')
        xml.write('\t<owner>\n')
        xml.write('\t\t<flickrid>NULL</flickrid>\n')
        xml.write('\t\t<name>ChaojieZhu</name>\n')
        xml.write('\t</owner>\n')
        xml.write('\t<size>\n')
        xml.write('\t\t<width>'+ str(width) + '</width>\n')
        xml.write('\t\t<height>'+ str(height) + '</height>\n')
        xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
        xml.write('\t</size>\n')
        xml.write('\t\t<segmented>1</segmented>\n')
        for multi in json_file["shapes"]:
            points = np.array(multi["points"])
            xmin = min(points[:,0])
            xmax = max(points[:,0])
            ymin = min(points[:,1])
            ymax = max(points[:,1])
            label = multi["label"]
            if xmax <= xmin:
                pass
            elif ymax <= ymin:
                pass
            else:
                xml.write('\t<object>\n')
                xml.write('\t\t<name>'+label+'</name>\n')
                xml.write('\t\t<pose>Unspecified</pose>\n')
                xml.write('\t\t<truncated>0</truncated>\n')
                xml.write('\t\t<difficult>0</difficult>\n')
                xml.write('\t\t<bndbox>\n')
                xml.write('\t\t\t<xmin>' + str(int(round(xmin))) + '</xmin>\n')
                xml.write('\t\t\t<ymin>' + str(int(round(ymin))) + '</ymin>\n')
                xml.write('\t\t\t<xmax>' + str(int(round(xmax))) + '</xmax>\n')
                xml.write('\t\t\t<ymax>' + str(int(round(ymax))) + '</ymax>\n')
                xml.write('\t\t</bndbox>\n')
                xml.write('\t</object>\n')
                print(json_filename, xmin, ymin, xmax, ymax, label)
        xml.write('</annotation>')