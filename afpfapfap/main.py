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


def scandirs(path):
    try:
        for entry in path.iterdir():
            try:
                #                 entry = sanitize(entry)

                # cleaners step

                cleaners = ExtensionManager('fapfap.cleaners',
                                            propagate_map_exceptions=True,
                                            on_load_failure_callback=cane,
                                            invoke_on_load=True)

                cleaners.map_method('sanitize', entry)

            except NukedFile:
                continue
            if entry.is_dir():
                yield from scandirs(entry)
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

    root_path = pathlib.Path(args.path)

    for entry in scandirs(root_path):
        print(entry.path)

    print(args)
