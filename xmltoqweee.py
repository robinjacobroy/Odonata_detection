import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


def convert_annotation(list_file):
    in_file = open(os.path.join(input_dir,fln))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if int(difficult)==1:
            continue
        cls_id = 0
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), \
             int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        

input_dir="/home/robin/dragon/damsel/train_xml/"        
out_file = open('/home/robin/train.txt', 'w')
for fln in os.listdir(input_dir):
    
    out_file.write("./train/"+fln.replace(".xml",".JPEG"))
    convert_annotation(out_file)
    out_file.write('\n')
out_file.close()
