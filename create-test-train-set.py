import os
import glob
from random import shuffle
import shutil
from math import floor


# Parameters
TRAINING_PERCENTAGE = 80
ORIGINAL_FOLDER = "processed"
CATEGORY_1 = "/one"
CATEGORY_2 = "/ten"
TRAIN_DESTINATION_FOLDER = "training"
TEST_DESTINATION_FOLDER = "test"


def get_file_list_from_dir(datadir):
    all_files = os.listdir(os.path.abspath(datadir))
    image_files = list(filter(lambda file: file.endswith('.JPG'), all_files))
    return image_files


def get_training_and_testing_sets(file_list):
    split = TRAINING_PERCENTAGE/100
    split_index = floor(len(file_list) * split)
    training = file_list[:split_index]
    testing = file_list[split_index:]
    return training, testing

def copy_training_and_testing_sets(image_folder, train_folder, test_folder):
    image_files = get_file_list_from_dir(image_folder)
    print image_folder, image_files
    training_files, testing_files = get_training_and_testing_sets(image_files)
    for original_file in training_files:
        shutil.copy(original_file,train_folder)
    for original_file in testing_files:
        shutil.copy(original_file, test_folder)


print "\n creating destination folders"
shutil.rmtree(TRAIN_DESTINATION_FOLDER, ignore_errors = True)
shutil.rmtree(TEST_DESTINATION_FOLDER, ignore_errors = True)

os.makedirs(TRAIN_DESTINATION_FOLDER+CATEGORY_1)
os.makedirs(TRAIN_DESTINATION_FOLDER+CATEGORY_2)
os.makedirs(TEST_DESTINATION_FOLDER)

print "\n Getting training and test for Category 1"
image_folder = ORIGINAL_FOLDER+CATEGORY_1
train_folder = TRAIN_DESTINATION_FOLDER + CATEGORY_1
test_folder = TEST_DESTINATION_FOLDER
copy_training_and_testing_sets(image_folder,train_folder,test_folder)

print "\n Getting training and test for Category 2"
image_folder = ORIGINAL_FOLDER+CATEGORY_2
train_folder = TRAIN_DESTINATION_FOLDER + CATEGORY_2
test_folder = TEST_DESTINATION_FOLDER
copy_training_and_testing_sets(image_folder,train_folder,test_folder)
