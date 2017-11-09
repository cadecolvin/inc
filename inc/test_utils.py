import os
import re

def get_test_filenames(path):
    """ Gets any filenames that follow the format [path]/[Tt]est_*.c """
    test_files = []
    for root, dirs, files in os.walk(path):
        [test_files.append(f) for f in files if f.lower().endswith('.c')]

    return [os.path.splitext(f)[0] for f in test_files]

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
