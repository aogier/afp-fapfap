'''
Created on 28/gen/2016

@author: oggei
'''


import os
import argparse
import logging
import pathlib


def sanitize(entry, suffix=''):

    # strip white spaces
    if entry.is_dir() and entry.name.strip() != entry.name:

        sanitized_path = os.path.join(os.path.dirname(entry.path),
                                      entry.name.strip() + suffix)

        try:
            os.rename(entry.path, sanitized_path)
        except OSError as e:
            # dir not empty
            if e.errno is 39:
                sanitize(entry, suffix + '_')
            else:
                raise OSError(e)
        logging.debug('stripped dir: "%s" -> "%s"',
                      entry.path, sanitized_path)
        entry = pathlib.Path(sanitized_path)

    return entry


class NukedFile(Exception):
    pass


def scandirs(path):
    try:
        for entry in path.iterdir():
            try:
                entry = sanitize(entry)
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
