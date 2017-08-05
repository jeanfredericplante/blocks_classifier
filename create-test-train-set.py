import os
import glob
import random
import numpy as np

import cv2

# Preprocessing images
TRAINING_PERCENTAGE = 80

train_folder = '/train/'
test_folder = '/test/'
category_1 = 'one'
category_2 = 'ten'

os.system('rm -rf  ' + train_lmdb)
os.system('rm -rf  ' + validation_lmdb)

ones_files = [img for img in glob.glob("../input/one/*.JPG")]
tens_files = [img for img in glob.glob("../input/ten/*.JPG")]

# Selecting test and training data
trainingsize_ones = TRAINING_PERCENTAGE * len(ones_files)
trainingsize_tens = TRAINING_PERCENTAGE * len(tens_files)
random.shuffle(ones_files)
random.shuffle(tens_files)

# Training and testing arrays
train_data = ones_files[:trainingsize_ones]+tens_files[:trainingsize_tens]
test_data = ones_files[trainingsize_ones+1:]+tens_files[trainingsize_tens+1:]
random.shuffle(train_data)
random.shuffle(test_data)

print '\n',len(ones_files)," number of ones images and ",len(tens_files), "number of tens images"
print 'concatenated training data ', len(train_data)
print 'concatenated test data ', len(test_data)
#for in_idx, img_path in enumerate(train_data):
#	if 'one' in img_path:
#		print 'this is a one file'
#	else:
#		print "this is a ten file"

#train_data = [img for img in glob.glob("../input/train/*jpg")]
#test_data = [img for img in glob.glob("../input/test1/*jpg")]
#
##Shuffle train_data
#random.shuffle(train_data)
#
print 'Creating train_lmdb'

in_db = lmdb.open(train_lmdb, map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, img_path in enumerate(train_data):
        if in_idx %  15 == 0: # don't have that much data
            continue
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
        if 'one' in img_path:
            label = 1
        else:
            label = 10
        datum = make_datum(img, label)
        in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
        print '{:0>5d}'.format(in_idx) + ':' + img_path
in_db.close()


print '\nCreating validation_lmdb'

in_db = lmdb.open(validation_lmdb, map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, img_path in enumerate(train_data):
        if in_idx % 6 != 0:
            continue
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
        if 'one' in img_path:
            label = 1
        else:
            label = 10
        datum = make_datum(img, label)
        in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
        print '{:0>5d}'.format(in_idx) + ':' + img_path
in_db.close()

print '\nFinished processing all images'
