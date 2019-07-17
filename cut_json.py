import json
import os

with open('', 'r') as f:
    annot_json = json.load(f)
filename = annot_json['imagePath']
filename = os.path.splitext(filename)[0]
left_annot = annot_json
left_annot['shapes'] = []
left_annot['imagePath'] = filename + '_left.png'
right_annot = annot_json
right_annot['imagePath'] = filename + '_right.png'
right_annot['shapes'] = []
