#!/usr/bin/env python3
'''
Created on 28/gen/2016

@author: oggei
'''


import os
import argparse
import logging
import pathlib
from stevedore.extension import ExtensionManager


class NukedFile(Exception):
    pass


def cane():
    a = 0 / 0

cleaners = ExtensionManager('fapfap.cleaners',
                            propagate_map_exceptions=True,
                            on_load_failure_callback=cane,
                            invoke_on_load=True)


def clean_dir(path, execute=False):
    try:
        for entry in path.iterdir():
            if entry.is_dir():
                print ('recurse into %s' % entry)
                clean_dir(entry, execute)

            for cleaner in cleaners:
                cleaner.obj.sanitize(entry, execute=execute)

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

    root_path = pathlib.Path(args.path)

    for entry in clean_dir(root_path, execute=args['execute']):
        print(entry.path)

    print(args)


if __name__ == '__main__':
    run()
