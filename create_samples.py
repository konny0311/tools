import cv2
import numpy as np
import json
import os

for i in range(1,20):
    for j in range(1,20):
        print(i, j)
        x = 50 * i
        y = 50 * j
        base_img = np.zeros((1000, 1000))
        img = cv2.circle(base_img, (x, y), 50, (255,255,255), -1)
        xmin = x - 50 if x > 50 else 0
        ymin = y - 50 if y > 50 else 0
        xmax = x + 50
        ymax = y + 50
        shape = {
            "label": "surfer",
            "shape_type": "rectangle"
        }
        shape['points'] = [[xmin, ymin], [xmax, ymax]]
        with open('sample.json', 'r') as f:
            content = json.load(f)
        content['shapes'] = [shape]
        name = 'circle{}_{}.jpg'.format(x,y)
        content['imagePath'] = name
        print(content)
        with open('circle_annots/' + name.replace('.jpg', '.json'), 'w') as f:
            json.dump(content, f)
        cv2.imwrite('circles/' + name, img)