import os,cv2,csv,argparse
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, \
help="directory of the predicted images with coordinate text files")
ap.add_argument("-o", "--output", required=True,\
help="directory to which the sobel masked image is to be stored")
args = vars(ap.parse_args())
            
            
input_dir=args['input']
out_dir=args['output']


for fln in sorted(os.listdir(input_dir)):
  if fln.endswith(".jpg"):
    im=cv2.imread(os.path.join(input_dir,fln))
    img=im.copy()
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
      im_crop=im[start_y:end_y,start_x:end_x].copy()
      
    
      ddepth = cv2.CV_16S
    
      src = cv2.GaussianBlur(im_crop, (3, 3), 0)
      gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
      # Gradient-X
      grad_x = cv2.Scharr(gray,ddepth,1,0)
      #grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
      # Gradient-Y
      grad_y = cv2.Scharr(gray,ddepth,0,1)
      #grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    
      abs_grad_x = cv2.convertScaleAbs(grad_x)
      abs_grad_y = cv2.convertScaleAbs(grad_y)
      grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    
      #thresholding the region inside the bounding box
      threshMap = cv2.threshold(grad \
                                , 0, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
      kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
      kernel1=np.ones((15,15),np.uint8)
      kernel2=np.ones((3,3),np.uint8)
      #morphological operations to make the object mask
      dilated=cv2.dilate(threshMap,kernel1,iterations=2)
      closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel1)
      eroded=cv2.erode(closing,kernel2,iterations=3)
      #draw the biggest contour, which could be the object
      _,contours,_=cv2.findContours(eroded,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
      drawing=np.ones(dilated.shape,np.uint8)*255
      drawing=cv2.cvtColor(drawing,cv2.COLOR_GRAY2BGR)
      c=max(contours,key=cv2.contourArea)
      cv2.drawContours(drawing,[c],0,(0,0,0),-1)
      
      final=cv2.bitwise_and(im_crop,drawing)
      final[np.where((final==[0,0,0]).all(axis=2))]= [255,0,255] 
      #output=cv2.hconcat([im_crop,final]) 
      #paste the masked region inside the cutout to the original image
      orig=Image.fromarray(img)
      cropped=Image.fromarray(final)
      orig.paste(cropped,(start_x,start_y))
      cv2.imwrite(os.path.join(out_dir,fln),np.uint8(orig))
      
