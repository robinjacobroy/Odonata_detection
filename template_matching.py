import os,shutil,csv,cv2
import numpy as np
import imutils

def rectangle(fpath):   
    img=cv2.imread(fpath)
    image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    template=cv2.imread(os.path.join(dir1+fld,fln),0)
    dims =np.array( template.shape[::-1])+100
    
    for num,scale in enumerate(np.linspace(0.2, 1.0, 10)[::-1]):
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        img_rez = imutils.resize(img, width = int(img.shape[1] * scale))
        resized = imutils.resize(image, width = int(image.shape[1] * scale))
        r_temp = imutils.resize(template, width = int(template.shape[1] * scale))
    
        w, h = r_temp.shape[::-1]
        res = cv2.matchTemplate(resized,r_temp,cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = min_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
    
        #this is w.r.t to the original image
        center=(top_left[0] + w//2, top_left[1] + h//2)
    
        
                    #y-axis start and end wrt the scaled image                
        imcrop=img_rez[center[1]-dims[1]//2:center[1]+dims[1]//2,\
                      center[0]-dims[0]//2:center[0]+dims[0]//2] #x-axis start and end
        if not (dims[1]-2<=imcrop.shape[0]<=dims[1]+2 and \
                dims[0]-2<=imcrop.shape[1]<=dims[0]+2) :
            continue
        edged=cv2.cvtColor(imcrop,cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(edged,r_temp,cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = min_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
    
        #cv2.rectangle(imcrop,top_left, bottom_right, (0,0,255), 3)
    
        cv2.imwrite(dir5+fln.replace(".jpg",'_%s.jpg'%(num+1)),imcrop)
        with open(os.path.join(dir5,fln.replace(".jpg",'_%s.txt'%(num+1))), "w") as boxfile:
            writer = csv.writer(boxfile)
            center_x=(top_left[0]+(w/2))/imcrop.shape[1]
            center_y=(top_left[1]+(h/2))/imcrop.shape[0]
            width=(w/imcrop.shape[1])
            height=(h/imcrop.shape[0])
            writer.writerow(["0 "+str(center_x)+" "+str(center_y)+" "+ str(width)+" "+ \
                             str(height)])


dir1="/home/robin/thumbi_out/train/"
dir2="/mnt/568A67711D6B5995/odonata/Field3-26062019/"
dir3="/mnt/568A67711D6B5995/odonata/Field3-Geetha2019/"
dir4="/mnt/568A67711D6B5995/odonata/Field3ACRoad11052019/"
dir5="/mnt/568A67711D6B5995/odonata/train_scaled/"

for fld in os.listdir(dir1):
    if (fld=="thumbi_11" or fld=="thumbi_12" or fld=="thumbi_13" or fld=="thumbi_14"):
        continue
    print(fld)
    for fln in os.listdir(dir1+fld):
        if os.path.exists(os.path.join(dir2,fln)):
            
            rectangle(os.path.join(dir2,fln))
            continue
        elif os.path.exists(os.path.join(dir3,fln)):
            rectangle(os.path.join(dir3,fln))
            continue
        elif os.path.exists(os.path.join(dir4,fln)):
            rectangle(os.path.join(dir4,fln))
            continue
        else:
            print("no such file exists {}".format(fln))
