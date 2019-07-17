import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir',help='directory path')
parser.add_argument('--save_file',help='save file path')
args = parser.parse_args()

if args.dir:
    files = glob.glob(os.path.join(args.dir, '*.xml'))
    files = sorted(files)
    for file in files:
        name = os.path.basename(file).replace('.xml', '')
        with open(args.save_file, 'a') as f:
            f.write(name + '\n')
        
