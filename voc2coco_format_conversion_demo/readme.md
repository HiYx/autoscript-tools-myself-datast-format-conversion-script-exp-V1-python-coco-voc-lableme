The data set is converted from VOC xml file to COCO format

stand by:
1. Parse the xml file and use import xml.etree.ElementTree as ET
2. Automatically obtain the categories in xml and convert them to uppercase to avoid confusion caused by uppercase and lowercase categories
3. Support error capture
4. Annotated files that support statistical errors (the value of bnbox is not a number)
5. Support checking the matching check of annotation files and images


数据集从VOC 的xml文件转换到COCO格式

支持：
1、解析xml文件，使用import xml.etree.ElementTree as ET
2、自动获取xml中的categories，并转换成大写，避免大小写的categories导致混乱
3、支持错误捕获
4、支持统计错误的标注文件（bnbox的值非数字）
5、支持检查标注文件和图像的匹配检查

xml包含了points和bndbox
```
<?xml version="1.0" encoding="UTF-8"?>
<annotation> 
  <worker>susu_008</worker>  
  <folder>li_bo</folder>  
  <filename>Cccc</filename>  
  <path>Cccc_Xml</path>  
  <source> 
    <database>unknown</database> 
  </source>  
  <size> 
    <width>950</width>  
    <height>674</height>  
    <depth>3</depth> 
  </size>  
  <segmented>0</segmented>  
  <object> 
    <name>noBrick_Inner_Parallel</name>  
    <type>polygon</type>  
    <uuid>3d595eb2-4dd0-43c1-9633-9390615141d8</uuid>  
    <attributes/>  
    <pose>Unspecified</pose>  
    <truncated>0</truncated>  
    <difficult>0</difficult>  
    <points> 
      <point> 
        <x>673.256146369354</x>  
        <y>165.087478559177</y> 
      </point>  
      <point> 
        <x>777.544311034877</x>  
        <y>169.432818753573</y> 
      </point>  
      <point> 
        <x>772.112635791881</x>  
        <y>455.138936535163</y> 
      </point>  
      <point> 
        <x>672.169811320755</x>  
        <y>448.620926243568</y> 
      </point> 
    </points> 
  </object>  
  <object> 
    <name>noBrick_Outer_Parallel</name>  
    <type>rectangle</type>  
    <uuid>375c5e9d-f958-458c-9e36-456f34fd3f84</uuid>  
    <attributes/>  
    <pose>Unspecified</pose>  
    <truncated>0</truncated>  
    <difficult>0</difficult>  
    <bndbox> 
      <xmin>659.133790737564</xmin>  
      <ymin>152.051457975986</ymin>  
      <xmax>789.493996569468</xmax>  
      <ymax>464.915951972556</ymax> 
    </bndbox> 
  </object> 
</annotation>
```

COCO
```
    json_dict = {"images":[],
                 "type": "instances",
                 "annotations": [],
                 "categories": []}
```

20210202