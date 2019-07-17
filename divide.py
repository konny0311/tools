import cv2
import numpy as np
import json
import os
import copy
import glob
from tqdm import tqdm

def create_save_upper_left(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    ori_h = img.shape[0]
    ori_w = img.shape[1]
    half_h = int(ori_h / 2)
    half_w = int(ori_w / 2)
    divided_img = img[0:half_h, 0:half_w]
    annot = copy.deepcopy(json_annot)
    annot['imageHeight'] = divided_img.shape[0]
    annot['imageWidth'] = divided_img.shape[1]
    annot['imageData'] = ''
    img_name = '{}_ul.png'.format(name)
    annot['imagePath'] = img_name
    shapes = annot['shapes']
    remain_ids = []
    for i, shape in enumerate(shapes):
        points = shape['points']
        x1 = points[0][0]
        x2 = points[1][0]
        y1 = points[0][1]
        y2 = points[1][1]
        xmin = x1 if x1 < x2 else x2
        ymin = y1 if y1 < y2 else y2
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        xmax = xmin + width
        ymax = ymin + height
        if is_inside_image([0,0,half_w,half_h], [xmin, ymin, xmax, ymax]): #pointsが切り取り画像内にある場合
            shape['points'] = [[xmin, ymin], [xmax, ymax]]
            remain_ids.append(i)

    shapes = [i for j, i in enumerate(shapes) if j in remain_ids]
    annot['shapes'] = shapes
    cv2.imwrite(os.path.join(divided_img_output_dir, img_name), divided_img)
    with open(os.path.join(annotation_output_dir, img_name.replace('.png', '.json')), 'w') as f:
        json.dump(annot,f)

def create_save_upper_right(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    ori_h = img.shape[0]
    ori_w = img.shape[1]
    half_h = int(ori_h / 2)
    half_w = int(ori_w / 2)
    divided_img = img[0:half_h, half_w:ori_w]
    annot = copy.deepcopy(json_annot)
    annot['imageHeight'] = divided_img.shape[0]
    annot['imageWidth'] = divided_img.shape[1]
    annot['imageData'] = ''
    img_name = '{}_ur.png'.format(name)
    annot['imagePath'] = img_name
    shapes = annot['shapes']
    remain_ids = []
    for i, shape in enumerate(shapes):
        points = shape['points']
        x1 = points[0][0]
        x2 = points[1][0]
        y1 = points[0][1]
        y2 = points[1][1]
        xmin = x1 if x1 < x2 else x2
        ymin = y1 if y1 < y2 else y2
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        xmax = xmin + width
        ymax = ymin + height
        if is_inside_image([half_w,0,ori_w,half_h], [xmin, ymin, xmax, ymax]): #pointsが切り取り画像内にある場合
            shape['points'] = [[xmin - half_w, ymin], [xmax - half_w, ymax]]
            remain_ids.append(i)

    shapes = [i for j, i in enumerate(shapes) if j in remain_ids]
    annot['shapes'] = shapes
    cv2.imwrite(os.path.join(divided_img_output_dir, img_name), divided_img)
    with open(os.path.join(annotation_output_dir, img_name.replace('.png', '.json')), 'w') as f:
        json.dump(annot,f)



def create_save_bottom_left(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    ORI_H = img.shape[0]
    ORI_W = img.shape[1]
    HALF_H = int(ORI_H / 2)
    HALF_W = int(ORI_W / 2)
    divided_img = img[HALF_H:ORI_H, 0:HALF_W]
    annot = copy.deepcopy(json_annot)
    annot['imageHeight'] = divided_img.shape[0]
    annot['imageWidth'] = divided_img.shape[1]
    annot['imageData'] = ''
    img_name = '{}_bl.png'.format(name)
    annot['imagePath'] = img_name
    shapes = annot['shapes']
    remain_ids = []
    for i, shape in enumerate(shapes):
        points = shape['points']
        x1 = points[0][0]
        x2 = points[1][0]
        y1 = points[0][1]
        y2 = points[1][1]
        xmin = x1 if x1 < x2 else x2
        ymin = y1 if y1 < y2 else y2
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        xmax = xmin + width
        ymax = ymin + height
        if is_inside_image([0,HALF_H,HALF_W,ORI_H], [xmin, ymin, xmax, ymax]): #pointsが切り取り画像内にある場合
            shape['points'] = [[xmin, ymin - HALF_H], [xmax, ymax - HALF_H]]
            remain_ids.append(i)

    shapes = [i for j, i in enumerate(shapes) if j in remain_ids]
    annot['shapes'] = shapes
    cv2.imwrite(os.path.join(divided_img_output_dir, img_name), divided_img)
    with open(os.path.join(annotation_output_dir, img_name.replace('.png', '.json')), 'w') as f:
        json.dump(annot,f)

def create_save_bottom_right(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    ori_h = img.shape[0]
    ori_w = img.shape[1]
    half_h = int(ori_h / 2)
    half_w = int(ori_w / 2)
    divided_img = img[half_h:ori_h, half_w:ori_w]
    annot = copy.deepcopy(json_annot)
    annot['imageHeight'] = divided_img.shape[0]
    annot['imageWidth'] = divided_img.shape[1]
    annot['imageData'] = ''
    img_name = '{}_br.png'.format(name)
    annot['imagePath'] = img_name
    shapes = annot['shapes']
    remain_ids = []
    for i, shape in enumerate(shapes):
        points = shape['points']
        x1 = points[0][0]
        x2 = points[1][0]
        y1 = points[0][1]
        y2 = points[1][1]
        xmin = x1 if x1 < x2 else x2
        ymin = y1 if y1 < y2 else y2
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        xmax = xmin + width
        ymax = ymin + height
        if is_inside_image([half_w,half_h,ori_w,ori_h], [xmin, ymin, xmax, ymax]): #pointsが切り取り画像内にある場合
            shape['points'] = [[xmin - half_w, ymin - half_h], [xmax - half_w, ymax - half_h]]
            remain_ids.append(i)

    shapes = [i for j, i in enumerate(shapes) if j in remain_ids]
    annot['shapes'] = shapes
    cv2.imwrite(os.path.join(divided_img_output_dir, img_name), divided_img)
    with open(os.path.join(annotation_output_dir, img_name.replace('.png', '.json')), 'w') as f:
        json.dump(annot,f)

def create_save_upper_center(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    ori_h = img.shape[0]
    ori_w = img.shape[1]
    half_h = int(ori_h / 2)
    half_w = int(ori_w / 2)
    img_xmin = int(half_w / 2)
    img_ymin = 0
    img_xmax = img_xmin + half_w
    img_ymax = half_h
    divided_img = img[img_ymin:img_ymax, img_xmin:img_xmax]
    annot = copy.deepcopy(json_annot)
    annot['imageHeight'] = divided_img.shape[0]
    annot['imageWidth'] = divided_img.shape[1]
    annot['imageData'] = ''
    img_name = '{}_uc.png'.format(name)
    annot['imagePath'] = img_name
    shapes = annot['shapes']
    remain_ids = []
    for i, shape in enumerate(shapes):
        points = shape['points']
        x1 = points[0][0]
        x2 = points[1][0]
        y1 = points[0][1]
        y2 = points[1][1]
        xmin = x1 if x1 < x2 else x2
        ymin = y1 if y1 < y2 else y2
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        xmax = xmin + width
        ymax = ymin + height
        if is_inside_image([img_xmin, img_ymin, img_xmax, img_ymax], [xmin, ymin, xmax, ymax]): #pointsが切り取り画像内にある場合
            shape['points'] = [[xmin - half_w, ymin - half_h], [xmax - half_w, ymax - half_h]]
            remain_ids.append(i)

    shapes = [i for j, i in enumerate(shapes) if j in remain_ids]
    annot['shapes'] = shapes
    cv2.imwrite(os.path.join(divided_img_output_dir, img_name), divided_img)
    with open(os.path.join(annotation_output_dir, img_name.replace('.png', '.json')), 'w') as f:
        json.dump(annot,f)

def create_save_bottom_center(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    ori_h = img.shape[0]
    ori_w = img.shape[1]
    half_h = int(ori_h / 2)
    half_w = int(ori_w / 2)
    img_xmin = int(half_w / 2)
    img_ymin = half_h
    img_xmax = img_xmin + half_w
    img_ymax = ori_h
    divided_img = img[img_ymin:img_ymax, img_xmin:img_xmax]
    annot = copy.deepcopy(json_annot)
    annot['imageHeight'] = divided_img.shape[0]
    annot['imageWidth'] = divided_img.shape[1]
    annot['imageData'] = ''
    img_name = '{}_bc.png'.format(name)
    annot['imagePath'] = img_name
    shapes = annot['shapes']
    remain_ids = []
    for i, shape in enumerate(shapes):
        points = shape['points']
        x1 = points[0][0]
        x2 = points[1][0]
        y1 = points[0][1]
        y2 = points[1][1]
        xmin = x1 if x1 < x2 else x2
        ymin = y1 if y1 < y2 else y2
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        xmax = xmin + width
        ymax = ymin + height
        if is_inside_image([img_xmin, img_ymin, img_xmax, img_ymax], [xmin, ymin, xmax, ymax]): #pointsが切り取り画像内にある場合
            shape['points'] = [[xmin - half_w, ymin - half_h], [xmax - half_w, ymax - half_h]]
            remain_ids.append(i)

    shapes = [i for j, i in enumerate(shapes) if j in remain_ids]
    annot['shapes'] = shapes
    cv2.imwrite(os.path.join(divided_img_output_dir, img_name), divided_img)
    with open(os.path.join(annotation_output_dir, img_name.replace('.png', '.json')), 'w') as f:
        json.dump(annot,f)


def is_inside_image(image_points_list, annot_points_list):
    if image_points_list[0] <= annot_points_list[0]:
        if annot_points_list[2] <= image_points_list[2]:
            if image_points_list[1] <= annot_points_list[1]:
                if annot_points_list[3] <= image_points_list[3]:
                    return True
    return False



def divide_into_4(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    create_save_bottom_left(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    create_save_bottom_right(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    create_save_upper_left(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    create_save_upper_right(img, json_annot, name, divided_img_output_dir, annotation_output_dir)

def divide_into_6(img, json_annot, name, divided_img_output_dir, annotation_output_dir):
    # create_save_bottom_left(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    # create_save_bottom_right(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    # create_save_upper_left(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    # create_save_upper_right(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    #TODO 上下真ん中2つメソッド作る
    create_save_upper_center(img, json_annot, name, divided_img_output_dir, annotation_output_dir)
    create_save_bottom_center(img, json_annot, name, divided_img_output_dir, annotation_output_dir)

if __name__ == '__main__':
    imgfiles = glob.glob(os.path.join('', '*.png'))
    annotation_dir = ''
    annotation_output_dir = ''
    divided_img_output_dir = ''
    pbar = tqdm(total=len(imgfiles), desc="dividing", unit=" files")
    for imgfile in imgfiles:
        name = os.path.basename(imgfile)
        name, _ = os.path.splitext(name)
        json_file = os.path.join(annotation_dir, '{}.json'.format(name))
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                json_annot = json.load(f)
            divide_into_6(cv2.imread(imgfile), json_annot, name, divided_img_output_dir, annotation_output_dir)
            pbar.update(1)
    pbar.close()