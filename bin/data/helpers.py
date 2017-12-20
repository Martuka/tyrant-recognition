from os import walk, path, remove
import sys
import openface
import cv2
import dlib
import pickle
import atexit
import glob
from time import time, strftime, localtime
from datetime import timedelta
import face_recognition



def get_files_list(tree):
    """
    Returns a list of paths for each image file in the tree
    rooting at path
    :param tree: the root of the tree from where to start
    :return: a list of path for image files
    """
    result = list()
    for (dir_path, _, file_names) in walk(tree):
        if file_names:
            for file in file_names:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    result.append(path.join(dir_path, file))

    return result

def dump_dict_to_db(dict, path_to_db):
    """
    Dumps a dictionary to a db file
    :param dict: the dict to write down to the file
    :return:
    """
    with open(path_to_db, mode='wb') as handle:
        pickle.dump(dict, handle)

def load_dict_from_db(path_to_db):
    """
    Returns a dictionary from a file
    :param path: the file path
    :return: the dictionary
    """
    with open(path_to_db, mode='rb') as handle:
        result = pickle.loads(handle.read())

    return result

def create_templates_database(dataset_path_list, db_file_path):
    """
    Writes templates from a dataset to a file for later reuse
    :param dataset_path:
    :param db_file_path:
    :return:
    """
    paths_list = dataset_path_list

    templates = dict()
    for file in paths_list:

        image = face_recognition.load_image_file(file)
        tmp = face_recognition.face_encodings(image)
        if tmp:
            template = face_recognition.face_encodings(image)[0]
            if template.size != 0:
                templates[file] = template

    dump_dict_to_db(templates, db_file_path)


def save_list_to_file(lst, filepath):
    with open(filepath, mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(' '.join(str(x) for x in tup) for tup in lst))
        myfile.write('\n')

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "=" * 40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog(start):
    end = time()
    elapsed = end - start
    log("End Program", secondsToStr(elapsed))


def listToFileByLines(lst, filepath):
    with open(filepath, mode='w', encoding='utf-8') as theFile:
        for x in lst:
            theFile.write(str(x[0]) + ' ' + str(x[1]) + '\n')


def deleteFilesInFolder(folder):
    files = glob.glob(folder + '/*')
    for f in files:
        remove(f)


def generate_landmark_files(folder, dim):

    # number of pixels for the edge of the resulting square image with the aligned face
    image_size = dim

    # You can download the required pre-trained face detection model here:
    # http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    predictor_model = "data/shape_predictor_68_face_landmarks.dat"

    # Take the image file name from the command line
    # file_name = "data/test/laurent.png"
    file_path = folder

    # Create a HOG face detector using the built-in dlib class
    face_detector = dlib.get_frontal_face_detector()
    face_pose_predictor = dlib.shape_predictor(predictor_model)
    face_aligner = openface.AlignDlib(predictor_model)

    for (dir_path, _, file_names) in walk(file_path):
        if file_names:
            for file_name in file_names:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    if (file_name+'.txt') not in file_names:
                        print('Current file: {}'.format(dir_path + '/' + file_name))
                        picture = path.join(dir_path, file_name)
                        # Load the image
                        image = cv2.imread(picture)

                        # Run the HOG face detector on the image data
                        detected_faces = face_detector(image, 1)

                        print("Found {} faces in the image file {}".format(len(detected_faces), picture))

                        face_rect = detected_faces[0]

                        # Detected faces are returned as an object with the coordinates
                        # of the top, left, right and bottom edges
                        print("- Face found at Left: {} Top: {} Right: {} Bottom: {}".format(face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

                        # Get the the face's pose
                        pose_landmarks = face_pose_predictor(image, face_rect)

                        landmarks = face_aligner.findLandmarks(image, face_rect)
                        listToFileByLines(landmarks, picture + '.txt')

                        # Use openface to calculate and perform the face alignment
                        alignedFace = face_aligner.align(image_size, image, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
