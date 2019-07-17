import os
import glob
import math
import cv2
import numpy as np
import PIL.Image as Image
from tqdm import tqdm


BASE_DIR = ''
ORIGIN_INPUTS_DIR = os.path.join(BASE_DIR, 'images')
ORIGIN_TEACHERS_DIR = os.path.join(BASE_DIR, 'npys')

INPUTS_DIR = os.path.join(BASE_DIR, 'inputs')
TEACHERS_DIR = os.path.join(BASE_DIR, 'teachers')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

SIZE_H = 512
SIZE_W = 512

ROTATE_CENTER_X = int(SIZE_W / 2)
ROTATE_CENTER_Y = int(SIZE_H / 2)


def main():
    files = glob.glob(os.path.join(ORIGIN_INPUTS_DIR, '*.jpg'))
    files.sort()
    print('### target annotation file : ', len(files))
    print('')
    counts = []
    pbar = tqdm(total=len(files), desc="Augmentaion", unit=" Files")
    for file in files:
        file_name, _ = os.path.splitext(os.path.basename(file))
        teacher_npy_path = os.path.join(ORIGIN_TEACHERS_DIR, file_name + '.npy')
        input_img = cv2.imread(file)

        if not os.path.exists(teacher_npy_path):
            print('teacher_npy is None : ', teacher_npy_path)
            continue
        teacher_npy = np.load(teacher_npy_path)
        count = image_data_augmentation(file_name, input_img, None, teacher_npy
                                        , rotate_stride=3
                                        , rotate_range=10
                                        )
        counts.append(count)
        pbar.update(1)
    pbar.close()

    if max(counts) == min(counts):
        print('')
        print('### augmentated all data : 1 --> ', max(counts))
    else:
        for count, file in zip(files, counts):
            file_name, _ = os.path.splitext(os.path.basename(file))
            print('### augmentate %s : 1 --> ' % file_name, count)


def image_data_augmentation(file_name, input_img, teacher_img, teacher_npy
                            , flip_type=None, scales=None, rotate_stride=None, rotate_range=None):
    bases = []
    bases.append((file_name + '_N', input_img, teacher_img, teacher_npy))
    if flip_type is not None:
        bases.append((file_name + '_F', cv2.flip(input_img, flip_type), cv2.flip(teacher_img, flip_type), teacher_npy))

    bases_2 = []
    if scales is None:
        scales = []
    for name, inp_img, tea_img, tea_npy in bases:
        bases_2.append((name + '_100', inp_img, tea_img, tea_npy))
        for scale in scales:
            bases_2.append((name + '_%03d' % (scale * 100), scaling_image(inp_img, scale), scaling_image(tea_img, scale), tea_npy))

    bases_3 = []
    if rotate_stride is None:
        rotate_stride = 360
    if rotate_range is None:
        rotate_range = 180
    rotate_start_degree = -rotate_range + (rotate_range % rotate_stride)
    rotate_end_degree = rotate_range - (rotate_range % rotate_stride) + 1
    for name, inp_img, tea_img, tea_npy in bases_2:
        bases_3.append((name + '_000', inp_img, tea_img, tea_npy))
        for k in range(rotate_start_degree, rotate_end_degree, rotate_stride):
            bases_3.append((name + '_%03d' % k, rotate_image(inp_img, k), "", rotate_npy(tea_npy, k, name + '_%03d' % k)))  # rotate_image(tea_img, k)

    data = bases_3
    for name, inp_img, tea_img, tea_npy in data:
        #print('data augmentation : ', name)
        input_save_path = os.path.join(INPUTS_DIR, name + '.png')
        # teacher_save_image_path = os.path.join(TEACHERS_DIR, name + '.png')
        teacher_save_npy_path = os.path.join(TEACHERS_DIR, name + '.npy')
        cv2.imwrite(input_save_path, inp_img)
        # cv2.imwrite(teacher_save_image_path, tea_img)
        # print('tea_npy read : ', tea_npy)
        np.save(teacher_save_npy_path, tea_npy)
#    print('### augmentation ', file_name, ' (1 -> ', len(data), ')')
    return len(data)


def scaling_image(img, scale):
    h, w, _ = np.shape(img)
    res_h, res_w = (math.floor(h * scale), math.floor(w * scale))
    img_resize = cv2.resize(img, (res_h, res_w))
    if scale < 1:
        #img_scale = np.zeros(np.shape(img))
        #pos_top = (h - res_h) // 2
        #pos_left = (w - res_w) // 2
        #img_scale[pos_top:pos_top+res_h,pos_left:pos_left+res_w,:] = img_resize
        h_tile_num = __calculate_tile_num(h, res_h)
        w_tile_num = __calculate_tile_num(w, res_w)
        img_tile = np.tile(img_resize, (h_tile_num, w_tile_num, 1))
        img_scale = __crop_image_center(img_tile, h, w)
    elif scale > 1:
        img_scale = __crop_image_center(img_resize, h, w)
    else:
        img_scale = img_resize
    return img_scale


def __calculate_tile_num(org_size, res_size):
    base = org_size / res_size
    if base - int(base) == 0:
        base = int(base)
        if base % 2 == 0:
            return base + 1
        else:
            return base
    else:
        return math.floor(base) + 2


def rotate_image(img, degree):
    pil_img_tile = Image.fromarray(np.uint8(img))
    pil_img_tile_rotate = pil_img_tile.rotate(degree, expand=False, resample=Image.BICUBIC)
    img_tile_rotate = np.array(pil_img_tile_rotate)

    img_rotate = __crop_image_center(img_tile_rotate, *(np.shape(img)[:2]))
    return img_rotate


def rotate_npy(img_npy, degree, name):
    rotated_npy = np.copy(img_npy)


    for i in range(0, len(img_npy)):
        point = img_npy[i, 1]  # ex. [255 285 308 394]
        # print(point)

        # cv2.rectangle(img, pt1, pt2, color, thickness=1, lineType=cv2.LINE_8, shift=0)
        zero_img_array = np.zeros((SIZE_H, SIZE_W), np.uint8)
        mask_square_img = cv2.rectangle(zero_img_array, (point[0], point[1]), (point[2], point[3]), 255)
        mask_img = Image.fromarray(np.uint8(mask_square_img))
        mask_img_rotate = mask_img.rotate(degree, expand=False)
        mask_npy_rotate = np.array(mask_img_rotate, dtype=np.uint8)
        contours = []
        for height in range(0, SIZE_H):
            for width in range(0, SIZE_W):
                if mask_npy_rotate[height, width] == 255:
                    contours.append([(width, height)])

        x, y, w, h = cv2.boundingRect(np.array(contours))
        rotated = [x, y, x+w, y+h]
        # print(rotated)
        rotated_npy[i, 1] = np.array(rotated)
        # circumscribed_rectangle_cv_img = cv2.rectangle(np.zeros((512, 512), np.uint8), (x, y), (x+w, y+h), 255)
        # circumscribed_rectangle_pil_img = Image.fromarray(np.uint8(circumscribed_rectangle_cv_img))
        # circumscribed_rectangle_pil_img.save(os.path.join(TEMP_DIR, name + '_' + str(i) + '_circumscribed.png'))

    return rotated_npy


def __crop_image_center(img, crop_h, crop_w):
    h, w = np.shape(img)[:2]
    pos_top = (h - crop_h) // 2
    pos_left = (w - crop_w) // 2
    return img[pos_top:pos_top+crop_h,pos_left:pos_left+crop_w,:]


if __name__ == '__main__':
    main()
