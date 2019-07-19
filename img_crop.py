import cv2, argparse,os
import numpy as np

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
    fname=fln.replace('.jpg','')    
    im=cv2.imread(os.path.join(input_dir,fln))
    cv2.namedWindow(fname, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(fname, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    r=[]
    r = cv2.selectROIs(fname,im)
    cv2.destroyAllWindows()    
    for i in range(0,len(r)):
            
        x=np.array(r[i])
        imCrop = im[int(x[1]):int(x[1]+x[3]), int(x[0]):int(x[0]+x[2])] 
        name1=fln.replace(".jpg",str(i)) 
        
        cv2.imwrite(os.path.join(out_dir,fln), imCrop)
   
