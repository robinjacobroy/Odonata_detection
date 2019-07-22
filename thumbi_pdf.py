import cv2,os
import numpy as np
import argparse
from PIL import Image
import pandas as pd

input_dir="/home/robin/thumbi/done/"
df=pd.read_csv("/home/robin/thumbi/Predictions_on_train_old.txt",header=None,sep=' ')
im_list=[]
for i in range(len(df)):
    
    h=df[1][i]
    name=h.rpartition("/")[-1]
    if os.path.exists(os.path.join(input_dir,name)):
        img=cv2.imread(os.path.join(input_dir,name))
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        cv2.putText(img,"predicted as %s with probability %f"%(df[5][i],df[10][i]),\
                    (10,30), cv2.FONT_HERSHEY_COMPLEX, .5,(0,0,0))
        
        im=Image.fromarray(img)
        im_list.append(im)
        
im.save("/home/robin/thumbi_out/try.pdf", "PDF" ,\
        resolution=100.0, save_all=True, append_images=im_list)
