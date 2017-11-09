import argparse
import ctypes
import glob
import os
import pathlib
import re
import shutil
import subprocess
import sys

def new(args):
    """ Logic behind the 'new' argument """
    project_dir = pathlib.Path(args.name)
    src_dir = pathlib.Path(project_dir.joinpath('src'))
    lib_dir = pathlib.Path(project_dir.joinpath('lib'))
    bin_dir = pathlib.Path(project_dir.joinpath('bin'))
    tst_dir = pathlib.Path(src_dir.joinpath('tests'))
    obj_dir = pathlib.Path(bin_dir.joinpath('obj'))

    src_dir.mkdir(parents=True, exist_ok=True)
    tst_dir.mkdir(parents=True, exist_ok=True)
    lib_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)
    obj_dir.mkdir(parents=True, exist_ok=True)

    # Deploy the default files
    deploy_makefile(args.name, project_dir.absolute())
    deploy_unittest(tst_dir.absolute())

def test(args):
    """ Logic behind the 'test' argument """
    # 1: Get all the filenames of the test files
    # 2: Compile each .c file into a .so file
    # 3: Load each .so file
    # 4: Parse the associated c file for test method names
    # 5: Execute each test method within the .so file


def main():
    parser = argparse.ArgumentParser(description='Manages and tests c projects')
    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser('new', help='Creates a new c project')
    parser_new.add_argument('name', help='The name of the new project')
    parser_new.set_defaults(func=new)

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
