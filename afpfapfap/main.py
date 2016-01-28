'''
Created on 28/gen/2016

@author: oggei
'''


import os
import argparse


def scandirs(path):
    try:
        for entry in os.scandir(path):

            print('check', entry.path)

            if entry.is_dir(follow_symlinks=False):
                yield from scandirs(entry.path)
            yield entry
    except PermissionError as e:
        print('perm error:', e)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='path to scan')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False, help='debug mode')
    parser.add_argument(
        '-x', '--execute', action='store_true', default=False, dest='real', help='execute for real')

    args = parser.parse_args()

    for entry in scandirs(args.path):
        print(entry.path)

    print(args)
