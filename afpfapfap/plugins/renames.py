'''
Created on 30/gen/2016

@author: oggei
'''
import os
import logging
import pathlib


ADDED_SUFFIX = '_'


class WhitespaceRemover(object):

    log_sanitized = 'stripped dir: "{0.name}" -> "{1.name}"'

    def sanitize(self, entry, suffix='', execute=False):

        stripped = entry.name.strip()

        if stripped != entry.name:

            sanitized_path = entry.parent.joinpath(stripped + suffix)

#             if sanitized_path.exists():
#                 self.sanitize(entry, suffix + ADDED_SUFFIX, execute)

            log = self.log_sanitized
            if not execute:
                log = 'DRY RUN: %s' % log
            else:

                if (entry.is_symlink()
                        or entry.is_socket()
                        or entry.is_fifo()
                        or entry.is_block_device()
                        or entry.is_char_device()):
                    logging.warn('special file {0.path} skipped'.format(entry))
                    return entry

                # directory rename
                elif entry.is_dir():

                    try:
                        # do the actual rename
                        entry.rename(sanitized_path)
                    except OSError as e:
                        # race condition: we tried to rename to an already
                        # existing, non-empty directory
                        if e.errno is 39:
                            # retry with a different suffix
                            self.sanitize(entry,
                                          suffix + ADDED_SUFFIX, execute)
                        else:
                            raise OSError(e)

                elif entry.is_file():

                    try:
                        # link is atomic and fails if target already exists
                        os.link(entry.path, sanitized_path.path)
                    except FileExistsError as e:
                        # race condition: we tried to create an already
                        # existing dir/file
                        if e.errno is 17:
                            # retry with a different suffix
                            self.sanitize(entry,
                                          suffix + ADDED_SUFFIX, execute)
                        else:
                            raise OSError(e)

                    # safely remove entry
                    entry.unlink()

                # rtfm ?
                else:
                    logging.critical(
                        'File {0.path} is neither a special nor a dir/file !'.format(entry))

            logging.warn(log.format(entry, sanitized_path))

            return sanitized_path
