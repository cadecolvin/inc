import ctypes
import glob
import os
import re


def get_test_files():
    files = glob.glob('*.so')
    file_names = [os.path.splitext(f)[0] for f in files]
    return [os.path.join(os.curdir, f) for f in file_names]

def get_test_functions(test_file):
    # Find the methods by parsing the associated .c file
    test_function_re = re.compile(r'(?:int )(test_.*)\(')
    functions = []

    with open(test_file + '.c', 'r') as f:
        for line in f:
            m = test_function_re.search(line)
            if m is not None:
                functions.append(m[1])

    return functions

if __name__ == '__main__':
    files = get_test_files();
    for f in files:
        test_functions = get_test_functions(f)
        test_file = ctypes.CDLL(f + '.so')
        for fun in test_functions:
            print('Running test...')
