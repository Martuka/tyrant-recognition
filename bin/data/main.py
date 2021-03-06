#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program uses the "face_recognition" python library
# https://github.com/ageitgey/face_recognition
#
# It will perform a 1:N face recognition comparing the selected image to our
# dictators and nobel prices facial database and find to which one it is the
# closest.

import face_recognition as fr
from helpers import *
import sys
import os
from shutil import copy
import random

# Replace False by True to recreate database, then put back to False
CREATE_DB = False
NB_RESULTS = 64

def main():
    """
    Do some stuff
    :return:
    """

    # Some benchmark stuff
    start = time()
    atexit.register(endlog, start)
    log("Start Python Program")

    # Create encodings database
    if CREATE_DB:
        files = get_files_list("data/dataset")
        create_templates_database(files, "db/dataset_facial_encodings.db")
    else:
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # cwd = os.getcwd()
        # log("dir_path = ", dir_path)
        # log("cwd = ", cwd)

        subject_picture_path = sys.argv[1]
        # subject_picture_path = "img/subject.png"
        subject = fr.load_image_file(subject_picture_path)

        # Get face encodings for each face in the image:
        subject_template = fr.face_encodings(subject)[0]

        known_templates_dict = load_dict_from_db("data/db/dataset_facial_encodings.db")

        temp = dict()

        for k, v in known_templates_dict.items():
            temp[k] = fr.face_distance([v], subject_template)

        result = sorted(temp.items(), key=lambda x: x[1][0])
        to_write = []
        to_copy = []
        for (path, delta) in result[:NB_RESULTS]:
            elems = path.split('/')
            name = elems[-2]
            tyrant = elems[-3]

            print(path, name, tyrant, ": delta = {}".format(delta[0]))
            to_write.append((path, name, tyrant, delta[0]))
            # if tyrant.endswith('rs'):
            to_copy.append(path)

        save_list_to_file(to_write, "data/results.txt")


        for img in to_copy[:6]:
            _, ext = os.path.splitext(img)
            dst = 'data/tmp/'+str(random.random())+ext
            print("copying {}\nto {}".format(img, dst))
            copy('data/'+img, dst)


if __name__ == "__main__":
    main()
