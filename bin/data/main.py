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

# Replace False by True to recreate databse, then put back to False
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
        files = get_files_list("data/all-included-set")
        create_templates_database(files, "db/named-set-templates.db")
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

        known_templates_dict = load_dict_from_db("data/db/named-set-templates.db")

        temp = dict()

        for k, v in known_templates_dict.items():
            temp[k] = fr.face_distance([v], subject_template)

        result = sorted(temp.items(), key=lambda x: x[1][0])
        to_write = []
        for (path, delta) in result[:NB_RESULTS]:
            name = path[path.rfind('/') + 1:path.rfind('-')]
            print(path, name, ": delta = {}".format(delta[0]))
            to_write.append((path, name, delta[0]))

        save_list_to_file(to_write, "data/results.txt")


if __name__ == "__main__":
    main()
