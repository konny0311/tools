import os
import glob
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--ori_dir',help='input image dir')
parser.add_argument('--save_dir',help='output dir for zip files')
parser.add_argument('--name',help='name of zip file')
args = parser.parse_args()

if not (args.ori_dir and args.save_dir):
    print('argument missing')
    exit()
else:
    ori_dir = args.ori_dir
    save_dir = args.save_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)        
    files = glob.glob(os.path.join(ori_dir, '*.jpg'))
    files += glob.glob(os.path.join(ori_dir, '*.png'))
    files = sorted(files)
    zip_name = args.name
    print(len(files))
    unit = 40
    max = int(len(files) / unit)
    for i in range(1, max + 2):
        if i == (max + 1):
            targets = files[unit * (i-1):]
        else:
            targets = files[unit * (i-1):unit * i]
        tmp_dir = os.path.join(save_dir, zip_name + str(i))
        os.makedirs(tmp_dir)
        for target in targets:
            name = os.path.basename(target)
            shutil.copyfile(target, os.path.join(tmp_dir, name))
        print(shutil.make_archive(os.path.join(save_dir, zip_name + '_%03d' % i), 'zip', root_dir = tmp_dir))



