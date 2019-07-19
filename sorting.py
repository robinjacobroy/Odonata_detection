import cv2,os,shutil
import numpy as np
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,help="directory of the cropped odonates")
ap.add_argument("-o", "--output", required=True,\
help="parent directory to which each one be stored")
args = vars(ap.parse_args())
            
            
input_dir=args['input']
out_dir=args['output']  


for i in range(14):
    vars()["dir"+str(i+1)]=out_dir+ 'thumbi_%s/'%str(i+1)
try:
    for i in range(14):
                
        os.mkdir(out_dir+ 'thumbi_%s/'%str(i+1))
        print("directory %s created"%(i+1))
except FileExistsError :
    print("Directories already exists")


for fln in sorted(os.listdir(input_dir)):
    fname=fln.replace(".jpg"," ")
    img=cv2.imread(os.path.join(input_dir,fln))
    cv2.namedWindow(fname, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(fname, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    cv2.imshow(fname,img)
    while(1):
        k=cv2.waitKey(0) & 0xFF
        if k==ord("a"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir1)
            break
        if k==ord("b"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir2)
            break
        if k==ord("c"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir3)
            break
        if k==ord("d"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir4)
            break
        if k==ord("e"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir5)
            break
        if k==ord("f"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir6)
            break
        if k==ord("g"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir7)
            break
        if k==ord("h"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir8)
            break
        if k==ord("i"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir9)
            break
        if k==ord("j"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir10)
            break 
        if k==ord("k"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir11) 
            break
        if k==ord("l"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir12) 
            break
        if k==ord("m"):
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir13) 
            break
        if k==27:
            cv2.destroyAllWindows()
            shutil.move(os.path.join(input_dir,fln),dir14) 
            break
        



