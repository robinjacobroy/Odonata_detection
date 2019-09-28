import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import argparse

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,help="directory of the xml file")
ap.add_argument("-o", "--output", required=True,\
help="directory to which YOLO format txt file to be stored")
args = vars(ap.parse_args())
            
            
input_dir=args['input']
out_dir=args['output']
for fln in sorted(os.listdir(input_dir)):
    
    
    in_file = open(os.path.join(input_dir,fln))
    out_file = open(os.path.join(out_dir,fln.replace("xml","txt")), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if int(difficult)==1:
            continue
        cls_id = 0
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    
    out_file.close()



