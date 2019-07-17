import os
import glob

DATA_DIR = os.path.join('', '')

target_files = []
target_files += glob.glob(os.path.join(DATA_DIR, '*.png'))
target_files += glob.glob(os.path.join(DATA_DIR, '*.PNG'))
target_files += glob.glob(os.path.join(DATA_DIR, '*.jpeg'))
target_files += glob.glob(os.path.join(DATA_DIR, '*.JPEG'))
target_files += glob.glob(os.path.join(DATA_DIR, '*.jpg'))
target_files += glob.glob(os.path.join(DATA_DIR, '*.JPG'))

target_files.sort()

start_id = 1

file_count = len(target_files)
print('### target_files : ', file_count)
for k, target_file in enumerate(target_files):
    counter = k + start_id
    dir_path = os.path.dirname(target_file)
    new_filename = 'renamed_%02d.jpg' % counter
    os.rename(target_file, os.path.join(DATA_DIR, new_filename))
    if counter % 50 == 0 or counter == file_count:
        print('renamed : %4d / %4d' % (counter, file_count) )

