import cv2
import os
import glob
import argparse

def convert(image_dir, ori_ext, out_ext):

    files = glob.glob(os.path.join(image_dir, '*.{}'.format(ori_ext)))
    new_dir = image_dir + '_{}'.format(out_ext)
    os.makedirs(new_dir)
    print(new_dir)
    for file in files:
        img = cv2.imread(file)
        name = os.path.basename(file)
        name = name.replace(ori_ext, out_ext)
        cv2.imwrite(os.path.join(new_dir, name), img)
        # os.remove(file)

parser = argparse.ArgumentParser(description='video_slice')
parser.add_argument('--dir',  type=str, help='image directory')
parser.add_argument('--ori_ext',  type=str, help='jpg or png')
parser.add_argument('--out_ext',  type=str, help='jpg or png')

args = parser.parse_args()

convert(args.dir, args.ori_ext, args.out_ext)