import argparse
import ctypes
import glob
import os
import pathlib
import re
import shutil
import subprocess
import sys

from inc import test_utils

def new(args):
    """ Logic behind the 'new' argument """
    # Create the directory structure names
    project_dir = pathlib.Path(args.name)
    src_dir = project_dir.joinpath('src')
    lib_dir = project_dir.joinpath('lib')
    bin_dir = project_dir.joinpath('bin')
    tst_dir = src_dir.joinpath('tests')
    obj_dir = bin_dir.joinpath('obj')

    # Build out the directory structure
    src_dir.mkdir(parents=True, exist_ok=True)
    tst_dir.mkdir(parents=True, exist_ok=True)
    lib_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)
    obj_dir.mkdir(parents=True, exist_ok=True)

    # Deploy the default files
    deploy_makefile(args.name, project_dir.absolute())
    deploy_unittest(tst_dir.resolve())

def test(args):
    """ Logic behind the 'test' argument """
    # Get the filenames of the test files
    src_dir = os.getcwd() + '/src'
    test_files = test_utils.get_test_files(src_dir)

    # For each test file compile the shared object and run tests
    for f in test_files:
        c_file = pathlib.Path(f)
        so_file = c_file.with_suffix('.so')
        subprocess.run(['gcc',c_file.resolve(),
                        '-fPIC','-shared','-o',so_file.absolute()]) 

        test_functions = test_utils.get_test_functions(c_file)
        test_file = ctypes.CDLL(so_file)
        for function in test_functions:
            test_file[function]()

        # Delete the .so file to reduce clutter
        so_file.unlink()

def main():
    parser = argparse.ArgumentParser(description='Manages and tests c projects')
    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser('new', help='Creates a new c project')
    parser_new.add_argument('name', help='The name of the new project')
    parser_new.set_defaults(func=new)

    parser_test = subparsers.add_parser('test', help='Runs unit tests')
    parser_test.set_defaults(func=test)

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit(1)

    args = parser.parse_args()
    args.func(args)

def deploy_makefile(target, path):
    """ Deploys a makefile to the path specified

    Args:
        target (str): Becomes the value of the makefile's TARGET variable
        path (str): The path to deploy the makefile to
    """
    files_dir = pathlib.Path(_get_files_dir())
    makefile_src = files_dir.joinpath('makefile')
    makefile_dst = pathlib.Path(path).joinpath('makefile')
    makefile_text = ''
    with open(makefile_src.absolute(), 'rt') as f:
        makefile_text = f.read()

    with open(makefile_dst.absolute(), 'wt') as f:
        f.write(makefile_text.replace('{target}', target))

def deploy_unittest(path):
    """ Deploys unittest.h to the path specified

    Args:
        path (str): The path to deploy unittest.h to
    """
    files_dir = pathlib.Path(_get_files_dir())
    unittest_src = files_dir.joinpath('unittest.h').absolute()
    unittest_dst = pathlib.Path(path).joinpath('unittest.h').absolute()
    shutil.copy(unittest_src, unittest_dst)

def _get_files_dir():
    """ Returns the full path to the included "files" directory """
    script_path = os.path.abspath(__file__)
    base_dir = pathlib.Path(os.path.dirname(script_path))
    files_dir = pathlib.Path(base_dir.joinpath('files'))
    return files_dir.absolute()
