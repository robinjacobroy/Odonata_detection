import sys
import cv2,os
import numpy as np
def sobel(im):
    
    window_name = ('Sobel - Simple Edge Detector')
    
    ddepth = cv2.CV_16S
    
    # Load the image
    src = cv2.imread(im, cv2.IMREAD_COLOR)
    image=src.copy()
    src = cv2.GaussianBlur(src, (3, 3), 0)
    
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # Gradient-X
    #grad_x = cv2.Scharr(gray,ddepth,1,0)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    # Gradient-Y
    grad_y = cv2.Scharr(gray,ddepth,0,1)
    #grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    #cv2.namedWindow("grad-x",cv2.WINDOW_NORMAL)
    #cv2.namedWindow("grd-y",cv2.WINDOW_NORMAL)
    #cv2.imshow("grd-x", abs_grad_x)
    #cv2.imshow("grad-y",abs_grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    threshMap = cv2.threshold(grad, 0, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    
    
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
    kernel1=np.ones((10,10),np.uint8)
    dilated=cv2.dilate(threshMap,kernel1,iterations=2)
    
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    _,contours,_=cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    drawing=np.zeros(dilated.shape,np.uint8)
    c=max(contours,key=cv2.contourArea)
    cv2.drawContours(drawing,[c],0,255,-1)
    final=cv2.bitwise_and(image,image,mask=drawing)
        
    #output=cv2.hconcat([image,final])
    name=im.rpartition("/")[-1]
    cv2.imwrite("/mnt/568A67711D6B5995/odonata/sobelout/{}".format(name),final)
    
    #cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    #cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    #cv2.imshow(window_name, output)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
input_dir="/home/robin/thumbi/test/"
for fl in os.listdir(input_dir):
    
    for fln in os.listdir(input_dir+fl):
        img=os.path.join(input_dir+fl,fln)
        sobel(img)
