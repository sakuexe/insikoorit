import os
import random
import shutil

ROOT_DIR = "trees_training"
TRAINING_PERCENTAGE = 80
TEST_DIR = "trees_valuation"


def move_files(filenames, from_dir, to_dir):
    class_name = os.path.basename(from_dir)
    new_dir = os.path.join(to_dir, class_name)

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    random.shuffle(filenames)

    for index, filename in enumerate(filenames):
        only_filename, file_extension = os.path.splitext(filename)
        new_filename = f"{class_name}_{index:03d}{file_extension.lower()}"

        shutil.move(os.path.join(from_dir, filename),
                    os.path.join(new_dir, new_filename))


for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    if not filenames:
        continue

    random.shuffle(filenames)

    # split into training and testing
    split_point = int((TRAINING_PERCENTAGE / 100) * len(filenames))

    training_files = filenames[:split_point]
    testing_files = filenames[split_point:]

    move_files(testing_files, dirpath, TEST_DIR)
    move_files(training_files, dirpath, ROOT_DIR)
