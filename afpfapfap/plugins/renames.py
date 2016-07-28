'''
Created on 30/gen/2016

@author: oggei
'''
import os
from afpfapfap import logging

log = logging.get('cleaner')

ADDED_SUFFIX = '_'


class Renamer(object):

    log_sanitized = 'Renamed :\n\t"{0.path}"\n\t"{1.path}"'

    def sanitize(self, entry, suffix='', execute=False):

        # strips out leading/trailing spaces
        # :2e become a dot
        # :2f become an underscore
        renamed = entry.name.strip().replace(':2e', '.').replace(':2f', '_').replace('::', ' ').replace(':', ' ')

        if renamed != entry.name:

            sanitized_path = entry.parent.joinpath(renamed + suffix)

            log_sanitized = self.log_sanitized
            if not execute:
                log_sanitized = 'DRY RUN: %s' % log_sanitized
            else:

                if (entry.is_symlink()
                        or entry.is_socket()
                        or entry.is_fifo()
                        or entry.is_block_device()
                        or entry.is_char_device()):
                    log.info('special file {0.path} skipped'.format(entry))
                    return entry

                # directory rename
                elif entry.is_dir():

                    try:
                        # do the actual rename
                        entry.rename(sanitized_path)
                    except OSError as e:
                        # race condition: we tried to rename to an already
                        # existing, non-empty directory

                        # NFS returns 17 even with dirs ...
                        if e.errno in (39, 17):
                            # retry with a different suffix
                            return self.sanitize(entry,
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
                            return self.sanitize(entry,
                                                 suffix + ADDED_SUFFIX, execute)
                        else:
                            raise OSError(e)

                    # safely remove entry
                    entry.unlink()

                # rtfm ?
                else:
                    log.critical(
                        'File {0.path} is neither a special nor a dir/file !'.format(entry))

            log.info(log_sanitized.format(entry, sanitized_path))

            return sanitized_path
