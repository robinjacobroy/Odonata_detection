import os,cv2,csv,argparse
import numpy as np

def crop_image(file_name):
    im=cv2.imread(file_name)
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

    #crop image
    im_crop=im[start_y:end_y,start_x:end_x]

    cv2.imwrite(os.path.join(out_dir,fln),im_crop)
    #cv2.namedWindow("hi",cv2.WINDOW_NORMAL)
    #cv2.imshow("hi",im_crop)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

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
        crop_image(os.path.join(input_dir,fln))
