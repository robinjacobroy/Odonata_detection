import os,cv2,csv,argparse
import numpy as np
from matplotlib import pyplot as plt


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, \
help="directory of the predicted images with coordinate text files")
ap.add_argument("-o", "--output", required=True,\
help="directory to which the cropped image is to be stored")
args = vars(ap.parse_args())
            
            
input_dir=args['input']
out_dir=args['output']


for fln in sorted(os.listdir(input_dir)):
  if fln.endswith(".jpg"):
    im=cv2.imread(os.path.join(input_dir,fln))
    #print(im.shape)
    W=im.shape[1]
    H=im.shape[0]
    lst=[]
    try:
      with open(os.path.join(input_dir,fln.replace(".jpg",".txt"))) as cs:
        red=csv.reader(cs,delimiter=' ')
        for itm in red:
          lst=list(map(float,itm))
    except:
      pass
    if not len(lst)==0:
  
      #center coordinates of the bounding box
      x=lst[1]*W
      y=lst[2]*H


      #width and height of the bounding box
      w=lst[3]*W
      h=lst[4]*H
      
      #start and end points of the bounding box
      start_x=int(x-w/2)
      start_y=int(y-h/2)

      end_x=int(x+w/2)
      end_y=int(y+w/2)

      #crop image
      im_crop=im[start_y:end_y,start_x:end_x]
      #plt.imsave(os.path.join(out_dir,fln),im_crop)
      cv2.imwrite(os.path.join(out_dir,fln),im_crop)
