import cv2
import numpy as np
import glob
import os

def trim_save(file, save_dir):
    img = cv2.imread(file)
    h = img.shape[0]
    trimmed = img[90:h-90, :]
    trimmed = cv2.cvtColor(trimmed, cv2.COLOR_BGR2GRAY)
    trimmed = cv2.threshold(trimmed, 100, 255, cv2.THRESH_BINARY)[1]
    name = os.path.basename(file)
    cv2.imwrite(os.path.join(save_dir, name), trimmed)

ori_dir = ''
save_dir = ''
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
files = glob.glob(os.path.join(ori_dir, '*.jpg'))
outs = [trim_save(file, save_dir) for file in files]