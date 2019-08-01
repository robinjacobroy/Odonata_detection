
import cv2, argparse,os
import numpy as np
import csv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,help="directory of the input image")
ap.add_argument("-o", "--output", required=True,\
help="directory to which the cropped image is to be stored")
args = vars(ap.parse_args())
            
            
input_dir=args['input']
out_dir=args['output']
for fln in sorted(os.listdir(input_dir)):
    if(os.path.exists(os.path.join(out_dir,fln))):
        print("cropping already done...")
        print("taking next image....")
        continue
    im_ext=fln.rpartition(".")[-1]
    fname=fln.replace(im_ext,'') 
    
    print(fln.rpartition(".")[-3])   
    im=cv2.imread(os.path.join(input_dir,fln))
    cv2.namedWindow(fname, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(fname, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    r=[]
    r = cv2.selectROIs(fname,im)
    print(r)
    cv2.destroyAllWindows()
    if len(r)==0:
        continue
    
        
        
    for i in range(0,len(r)):
        with open(os.path.join(out_dir,fln.replace(im_ext,'txt')), "a") as boxfile:
            writer = csv.writer(boxfile)
            center_x=(r[i][0]+(r[i][2]/2))/im.shape[1]
            center_y=(r[i][1]+(r[i][3]/2))/im.shape[0]
            width=(r[i][2]/im.shape[1])
            height=(r[i][3]/im.shape[0])
            writer.writerow(["0 "+str(center_x)+" "+str(center_y)+" "+ str(width)+" "+ str(height)]) 
            
        x=np.array(r[i])
        imCrop = im[int(x[1]):int(x[1]+x[3]), int(x[0]):int(x[0]+x[2])] 
        
        
        if(len(r)>1):
            name1=fln.replace(fln.rpartition(".")[-3],fln.rpartition(".")[-3]+"_"+str(i)) 
            print(name1)
            cv2.imwrite(os.path.join(out_dir,name1), imCrop)
        else:
            cv2.imwrite(os.path.join(out_dir,fln), imCrop)



                     
    
