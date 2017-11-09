import argparse
import os
import pathlib
import sys

from inc import files


def new(args):
    """ Logic behind the 'new' argument """

    # Create the project and default subdirectories
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
    deploy_makefile(args.name, project_dir)

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

def deploy_makefile(project_name, project_path):
    makefile = project_path.joinpath('makefile')
    makefile_text = files.makefile.format(target=project_name)
    with open(makefile, 'wt') as f:
        f.write(makefile_text)
