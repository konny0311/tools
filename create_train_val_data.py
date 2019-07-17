import os
import glob
import sys
import random
import shutil
import argparse

def create_txt(ori_dir, output_dir):
    train_output_path = os.path.join(output_dir, 'train.txt')
    val_output_path = os.path.join(output_dir, 'val.txt')
    # files = glob.glob(os.path.join(ori_dir, '*.json'))
    files = glob.glob(os.path.join(ori_dir, '*.jpg'))
    files += glob.glob(os.path.join(ori_dir, '*.png'))
    random.shuffle(files)
    cnts = len(files)
    train_cnts = int(cnts * 0.8)
    with open(train_output_path, 'a') as f:
        for file in files[:train_cnts]:
            file = os.path.basename(file).replace('.json', '').replace('.jpg', '').replace('.png', '')
            # file = file.split('/')[-1].replace('.jpg', '').replace('.png', '')
            f.write(file + '\n')
    print(train_cnts)
    print('train done!')
    with open(val_output_path, 'a') as f:
        for file in files[train_cnts:]:
            file = os.path.basename(file).replace('.json', '').replace('.jpg', '').replace('.png', '')
            # file = file.split('/')[-1].replace('.jpg', '').replace('.png', '')
            f.write(file + '\n')
    print(cnts - train_cnts)    
    print('val done!')

def create_dir(img_ori_dir, annot_ori_dir, output_dir):
    files = glob.glob(os.path.join(img_ori_dir, '*.png'))
    files += glob.glob(os.path.join(img_ori_dir, '*.jpg'))
    ext = '.png'
    random.shuffle(files)
    cnts = len(files)
    train_cnts = int(cnts * 0.8)
    train_img_dir = os.path.join(output_dir, 'train_inputs')
    train_annot_dir = os.path.join(output_dir, 'train_teachers')
    val_img_dir = os.path.join(output_dir, 'val_inputs')
    val_annot_dir = os.path.join(output_dir, 'val_teachers')
    for dir in [train_img_dir, train_annot_dir, val_img_dir, val_annot_dir]:
        if not os.path.exists(dir):
            os.mkdir(dir)
    for file in files[:train_cnts]:
        filename = os.path.basename(file)
        filename, _ = os.path.splitext(filename)
        shutil.copyfile(file, os.path.join(train_img_dir, filename + ext))
        shutil.copyfile(os.path.join(annot_ori_dir, filename + ext), os.path.join(train_annot_dir, filename + ext))
    print('train done')
    for file in files[train_cnts:]:
        filename = os.path.basename(file)
        filename, _ = os.path.splitext(filename)
        shutil.copyfile(file, os.path.join(val_img_dir, filename + ext))
        shutil.copyfile(os.path.join(annot_ori_dir, filename + ext), os.path.join(val_annot_dir, filename + ext))
    print('val done')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='video_slice')
    parser.add_argument('--type',  type=str, help='output txt or dir')
    parser.add_argument('--img_ori', type=str, help='image origin dir')
    parser.add_argument('--annot_ori', type=str, help='annotation origin dir')
    parser.add_argument('--output', type=str, help='output dir')
    
    args = parser.parse_args()

    if args.type == 'txt':
        create_txt(args.img_ori, args.output)
    if args.type == 'dir':
        create_dir(args.img_ori, args.annot_ori, args.output)

