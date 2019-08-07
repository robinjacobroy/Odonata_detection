import os,shutil,csv,cv2

def rectangle(fpath):       
    im = cv2.imread(fpath)
    img=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    template = cv2.imread(os.path.join(dir1+fld,fln),0)
    w, h = template.shape[::-1]
    img = img2.copy()
    method=eval('cv2.TM_SQDIFF_NORMED')
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(im,top_left, bottom_right, (0,255,255), 5)
    cv2.imwrite(dir5+fln,im)
    with open(os.path.join(dir5,fln.replace("jpg",'txt')), "w") as boxfile:
        writer = csv.writer(boxfile)
        center_x=(top_left[0]+(w/2))/img.shape[1]
        center_y=(top_left[1]+(h/2))/img.shape[0]
        width=(w/img.shape[1])
        height=(h/img.shape[0])
        writer.writerow(["0 "+str(center_x)+" "+str(center_y)+" "+ str(width)+" "+ \
                         str(height)]) 



dir1="/home/robin/thumbi_out/train/"
dir2="/mnt/568A67711D6B5995/odonata/Field3-26062019/"
dir3="/mnt/568A67711D6B5995/odonata/Field3-Geetha2019/"
dir4="/mnt/568A67711D6B5995/odonata/Field3ACRoad11052019/"
dir5="/mnt/568A67711D6B5995/odonata/train_field3/"

for fld in os.listdir(dir1):
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
