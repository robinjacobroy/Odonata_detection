import os,cv2,csv,argparse
import numpy as np
from PIL import Image

def crop_image(file_name):
    im=cv2.imread(file_name)
    img=im.copy()
    W=im.shape[1]
    H=im.shape[0]

    with open(file_name.replace(".jpg",".txt")) as cs:
        red=csv.reader(cs,delimiter=' ')
        for itm in red:
            itm=list(map(float,itm))

    #center coordinates of the bounding box
    x=itm[1]*W
    y=itm[2]*H


    #width and height of the bounding box
    w=itm[3]*W
    h=itm[4]*H

    #start and end points of the bounding box
    start_x=int(x-w/2)
    start_y=int(y-h/2)

    end_x=int(x+w/2)
    end_y=int(y+w/2)

    #cropped image
    im_crop=im[start_y:end_y,start_x:end_x].copy()
    im[start_y:end_y,start_x:end_x]=[255,0,255]
    im[np.where((im!=[255,0,255]).all(axis=2))]= [255,255,255]
    im[np.where((im==[255,0,255]).all(axis=2))]= [0,0,0]
    im[np.where((im!=[0,0,0]).all(axis=2))]= [255,255,255]
    im=np.invert(im)
    masked=cv2.bitwise_and(img,im)
    
    ddepth = cv2.CV_16S
    
    src = cv2.GaussianBlur(im_crop, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # Gradient-X
    #grad_x = cv2.Scharr(gray,ddepth,1,0)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    # Gradient-Y
    grad_y = cv2.Scharr(gray,ddepth,0,1)
    #grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    threshMap = cv2.threshold(grad \
                              , 0, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    
    
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
    kernel1=np.ones((10,10),np.uint8)
    dilated=cv2.dilate(threshMap,kernel1,iterations=2)
    
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    _,contours,_=cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    drawing=np.zeros(dilated.shape,np.uint8)
    c=max(contours,key=cv2.contourArea)
    cv2.drawContours(drawing,[c],0,255,-1)
    final=cv2.bitwise_and(im_crop,im_crop,mask=np.invert(drawing))
        
    #output=cv2.hconcat([im_crop,final])
    orig=Image.fromarray(img)
    cropped=Image.fromarray(final)
    orig.paste(cropped,(start_x,start_y))
    cv2.imwrite(os.path.join(out_dir,fln),np.uint8(orig))
    
                
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, \
help="directory of the predicted images with coordinate text files")
ap.add_argument("-o", "--output", required=True,\
help="directory to which the masked odonates are to be stored")
args = vars(ap.parse_args())
            
            
input_dir=args['input']
out_dir=args['output']
for fln in sorted(os.listdir(input_dir)):
    if fln.endswith(".jpg"):
        crop_image(os.path.join(input_dir,fln))
