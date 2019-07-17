import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='video_slice')
parser.add_argument('--ori', dest='original image', type=str, help='original')
parser.add_argument('--ins', dest='inspection image', type=str, help='inspection')
args = parser.parse_args()

ori_img = cv2.imread('')
ins_img = cv2.imread('')
RATIO = 0.7

detector = cv2.AKAZE_create()
ori_kp, ori_desc = detector.detectAndCompute(ori_img, None)
ins_kp, ins_desc = detector.detectAndCompute(ins_img, None)

matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = matcher.knnMatch(ori_desc, ins_desc, k=2)
good = []
for m, n in matches:
    if m.distance < RATIO * n.distance:
        good.append(m)

if len(good) > 0:
    src_pts = np.float32([ ori_kp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ ins_kp[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w,_ = ori_img.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    x1, y1, x2, y2 = int(dst[0][0][0]), int(dst[0][0][1]), int(dst[2][0][0]), int(dst[2][0][1])
    print(x1, y1, x2, y2)
    # x1 = 0 if x1 < 0 else x1
    # y1 = 0 if y1 < 0 else y1
    new_img = cv2.resize(np.zeros((1, 1, 3), np.uint8), (x2 - x1, y2 - y1))
    new_img[abs(y1):, abs(x1):] = ins_img[0:y2, 0:x2]
    new_img = cv2.resize(new_img, (w, h))
    cv2.imwrite('new.png', new_img)
    # ins_img = ins_img[y1:y2, x1:x2]
    # ins_img = cv2.resize(ins_img, (w, h))

    # ori_hsv = cv2.split(cv2.cvtColor(ori_img, cv2.COLOR_BGR2HSV))
    # ins_hsv = cv2.split(cv2.cvtColor(ins_img, cv2.COLOR_BGR2HSV))
    # cv2.imwrite('test_h.png', ori_hsv[0])
    # cv2.imwrite('test_s.png', ori_hsv[1])
    # cv2.imwrite('ori_v.png', ori_hsv[2])
    # cv2.imwrite('ins_v.png', ins_hsv[2])

    ori_gray = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
    # ins_gray = cv2.cvtColor(ins_img, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(ori_gray, new_gray)
    # diff = cv2.threshold(diff, 100, 200, cv2.THRESH_BINARY)[1]
    # kernel = np.ones((3, 3), np.uint8)
    # diff = cv2.erode(diff, kernel, iterations=2)
    # diff = cv2.dilate(diff, kernel)
    cv2.imwrite('diff_gray.png', diff)

else:
    print('not matched')
    exit()

