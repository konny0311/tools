import os
import glob
import json
import cv2
import numpy as np
import pprint
import colorsys
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from tqdm import tqdm

BASE_DIR = ''
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
ANNOTAION_DIR = os.path.join(BASE_DIR, 'annotations')
REGION_DIR = os.path.join(BASE_DIR, 'regions')
OVERLAY_DIR = os.path.join(BASE_DIR, 'overlay')
TEACHER_DIR = os.path.join(BASE_DIR, 'npys')

SIZE_H = 512
SIZE_W = 512
REGION_COLOR = (0, 1, 0)
REGION_TH = 10 #90

CLASS_LIST = [
            'class1'
             ]


def main():
    files = glob.glob(os.path.join(ANNOTAION_DIR, '*.json'))
    files.sort()
    print('### target annotation file : ', len(files))
    print('')

    pbar = tqdm(total=len(files), desc="Create", unit=" Files")
    for k, file in enumerate(files):
        create_annotation_img(file)
        pbar.update(1)
    pbar.close()


def create_annotation_img(anno_json):
    jf = json.load(open(anno_json))
    image_name_base, _ = os.path.splitext(os.path.basename(anno_json))

    original_image_path = os.path.join(IMAGE_DIR, image_name_base)
    org_img = cv2.imread(original_image_path + '.png')
    if org_img is None:
        org_img = cv2.imread(original_image_path + '.jpg')
    org_img = org_img.astype(np.uint8)
    img_h, img_w, img_c = np.shape(org_img)
    org_img = cv2.resize(org_img, (SIZE_H, SIZE_W))
    ratio_h = SIZE_H / img_h
    ratio_w = SIZE_W / img_w

    seg_img = None
    teacher_vecs = []
    reg_colors = random_colors(len(CLASS_LIST))
    for k, shape in enumerate(jf['shapes']):
        contours = shape['points']
        if not shape['label'] in CLASS_LIST:
            continue

        label_idx = 0
        one_hot_vec = np.repeat([0], 1 + len(CLASS_LIST))
        for k, c in enumerate(CLASS_LIST):
            if shape['label'] == c:
                one_hot_vec[k + 1] = 1
                label_idx = k
                break

        mask = np.array(contours)
        if len(mask) < 2:
            print('mask region is None : ', image_name_base, '[%2d]' % k)
            continue
        mask = resize_mask(ratio_h, ratio_w, mask)
        img, region = create_region_image((SIZE_H, SIZE_W, 3), mask, reg_color=reg_colors[label_idx])
        #img, region = create_region_image(np.shape(org_img), mask)
        if img is None:
            continue

        teacher_vec = np.array([one_hot_vec, np.array(region)])
        teacher_vecs.append(teacher_vec)

        file_name = '%s_%d.png' % (image_name_base, k)
        file_path = os.path.join(REGION_DIR, file_name)
        cv2.imwrite(file_path, img)

        if seg_img is None:
            seg_img = img
        else:
            seg_img += img
            seg_img[seg_img > 255] = 255

    if seg_img is None:
        print('seg_img is None. : ', image_name_base)
        return

    teacher_numpy_file = os.path.join(TEACHER_DIR, image_name_base + '.npy')
    np.save(teacher_numpy_file, teacher_vecs)

    seg_img = seg_img.astype(np.uint8)
    segmentation_path = os.path.join(REGION_DIR, image_name_base + '_all' + '.png')
    seg_img_resize = seg_img
    cv2.imwrite(segmentation_path, seg_img_resize)

    overlay_ing = cv2.addWeighted(org_img, 1, seg_img, 1, 0)
    overlay_path = os.path.join(OVERLAY_DIR, image_name_base + '.png')
    overlay_ing_resize = overlay_ing
    cv2.imwrite(overlay_path, overlay_ing_resize)


def resize_mask(ratio_h, ratio_w, mask):
    new_mask = np.array(mask, dtype='float32')
    new_mask[:, 0] *= ratio_w
    new_mask[:, 1] *= ratio_h
    new_mask = new_mask.astype('int32')
    return new_mask


def create_region_image(image_shape, mask, reg_color=REGION_COLOR):
    img_src = np.zeros((image_shape[0], image_shape[1], 3))
    x, y, w, h = cv2.boundingRect(mask)
    img = cv2.rectangle(img_src, (x, y), (x+w, y+h), reg_color, 4)
    #img = img * 255
    region_size = w * h
    if region_size < REGION_TH:
        return None, None
    return img, (x, y, x+w, y+h)


def random_colors(N):
    rgb_colors = []
    for i in range(N):
        hsv = i/N, 0.8, 1.0
        rgb = colorsys.hsv_to_rgb(*hsv)
        rgb = tuple((int(val * 255) for val in rgb))
        rgb_colors.append(rgb)
    return rgb_colors


if __name__ == '__main__':
    main()
