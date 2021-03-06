#!/usr/bin/env python3
'''
Created on 28/gen/2016

@author: oggei
'''

import argparse
import pathlib
from stevedore.extension import ExtensionManager
from afpfapfap import logging

log = logging.get('cleaner')


class NukedFile(Exception):
    pass


def cane(*args):
    print('ciao', args)
    a = 0 / 0

cleaners = ExtensionManager('fapfap.cleaners',
                            propagate_map_exceptions=True,
                            on_load_failure_callback=cane,
                            invoke_on_load=True)

removers = ExtensionManager('fapfap.removers',
                            propagate_map_exceptions=True,
                            on_load_failure_callback=cane,
                            invoke_on_load=True)


def clean_dir(path, execute=False):
    log.debug('Entering dir: %s', path)
    try:
        for entry in path.iterdir():
            if entry.is_dir():
                log.debug('Recurse into: %s', entry)
                clean_dir(entry, execute)

            for remover in removers:
                try:
                    remover.obj.sanitize(entry, execute=execute)
                except NukedFile:
                    break
            else:
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
        '-x', '--execute', action='store_true', default=False, dest='execute', help='execute for real')

    args = parser.parse_args()

    root_path = pathlib.Path(args.path)

    clean_dir(root_path, execute=args.execute)


if __name__ == '__main__':
    run()
