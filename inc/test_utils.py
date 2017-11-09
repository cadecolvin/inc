import os
import pathlib
import re

def get_test_files(path):
    """ Recursively searches path for any filenames that follow the format test_*.c """

    test_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if('test_' in f.lower() and f.lower().endswith('.c')):
                test_files.append(os.path.join(root, f))

    return test_files

def get_test_functions(test_file):
    # Find the methods by parsing the associated .c file
    test_function_re = re.compile(r'(?:void )(test_.*)\(')
    functions = []

    with open(test_file, 'r') as f:
        for line in f:
            m = test_function_re.search(line)
            if m is not None:
                functions.append(m[1])

    return functions
