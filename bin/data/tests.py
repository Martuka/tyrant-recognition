import sys
from os import walk
from helpers import *




def main():

    start = time()
    atexit.register(endlog, start)
    log("Start Python Program")

    path = sys.argv[0]

    for (dir_path, _, file_names) in walk(path):
        if file_names:
            for file in file_names:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):




