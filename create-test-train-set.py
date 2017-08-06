import os
import glob
from random import shuffle
import shutil
from math import floor
import sys


# Parameters
TEST_PERCENTAGE = 20.0
VALIDATION_PERCENTAGE = 10.0
ORIGINAL_FOLDER = "processed"
CATEGORY_1 = "/one"
CATEGORY_2 = "/ten"
TRAIN_DESTINATION_FOLDER = "training"
TEST_DESTINATION_FOLDER = "test"
VALIDATION_DESTINATION_FOLDER = "valid"


def get_file_list_from_dir(datadir):
    all_files = os.listdir(os.path.abspath(datadir))
    image_files = list(filter(lambda file: file.endswith('.JPG'), all_files))
    return image_files


def get_training_validation_testing_sets(file_list, validation_ratio, testing_ratio):
    train_split = 1 - validation_ratio - testing_ratio
    if train_split <= 0:
        sys.exit("Your train and test percentage sum can't be greater than 100 pct")
    train_split_index = int(floor(len(file_list) * train_split))
    valid_split_index = int(floor(len(file_list) * validation_ratio)) + train_split_index
    print "..Total size: ", len(file_list)
    print "...Training size: ", train_split_index
    print "...Validation size: ", valid_split_index - train_split_index
    print "...Testing size: ", len(file_list)-valid_split_index

    training = file_list[:train_split_index]
    validating = file_list[train_split_index+1:valid_split_index]
    testing = file_list[valid_split_index+1:]
    return training, validating, testing

def copy_training_and_testing_sets(image_folder, train_folder, validation_folder, test_folder):
    image_files = get_file_list_from_dir(image_folder)
    validation_ratio = VALIDATION_PERCENTAGE / 100
    testing_ratio = TEST_PERCENTAGE / 100
    shuffle(image_files)
    training_files, validation_files, testing_files = get_training_validation_testing_sets(image_files, validation_ratio, testing_ratio)
    for original_file in training_files:
        shutil.copy(image_folder + '/' + original_file, train_folder)
    for original_file in validation_files:
        shutil.copy(image_folder + '/' + original_file, validation_folder)
    for original_file in testing_files:
        shutil.copy(image_folder + '/' + original_file, test_folder)


print "\nCreating destination folders"
shutil.rmtree(TRAIN_DESTINATION_FOLDER, ignore_errors = True)
shutil.rmtree(TEST_DESTINATION_FOLDER, ignore_errors = True)
shutil.rmtree(VALIDATION_DESTINATION_FOLDER, ignore_errors = True)

os.makedirs(TRAIN_DESTINATION_FOLDER+CATEGORY_1)
os.makedirs(TRAIN_DESTINATION_FOLDER+CATEGORY_2)
os.makedirs(VALIDATION_DESTINATION_FOLDER+CATEGORY_1)
os.makedirs(VALIDATION_DESTINATION_FOLDER+CATEGORY_2)
os.makedirs(TEST_DESTINATION_FOLDER)

print "\nGetting training, validation and test for Category 1"
image_folder = ORIGINAL_FOLDER+CATEGORY_1
train_folder = TRAIN_DESTINATION_FOLDER + CATEGORY_1
validation_folder = VALIDATION_DESTINATION_FOLDER + CATEGORY_1
test_folder = TEST_DESTINATION_FOLDER
copy_training_and_testing_sets(image_folder,train_folder, validation_folder, test_folder)

print "\nGetting training, validation and test for Category 2"
image_folder = ORIGINAL_FOLDER+CATEGORY_2
train_folder = TRAIN_DESTINATION_FOLDER + CATEGORY_2
validation_folder = VALIDATION_DESTINATION_FOLDER + CATEGORY_2
test_folder = TEST_DESTINATION_FOLDER
copy_training_and_testing_sets(image_folder,train_folder, validation_folder, test_folder)
