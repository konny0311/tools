import cv2
import os
import glob

SIZE = 512
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (SIZE, SIZE))
img_dir = ''
imgfiles = glob.glob(os.path.join(img_dir, '*.png'))
print(len(imgfiles))
for i, imgfile in enumerate(imgfiles):
    print(i)
    img = cv2.imread(imgfile)
    img = cv2.resize(img, (SIZE, SIZE))
    out.write(img)
out.release()
