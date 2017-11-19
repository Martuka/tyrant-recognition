from os import walk, path
import pickle
import atexit
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




# files = get_files_list("data/all-included-set")
# create_templates_database(files, "db/named-set-templates.db")
