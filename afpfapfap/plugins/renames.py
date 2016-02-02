'''
Created on 30/gen/2016

@author: oggei
'''
import os
import logging
import pathlib


class WhitespaceRemover(object):

    def sanitize(self, entry, suffix=''):

        # strip white spaces
        if entry.is_dir() and entry.name.strip() != entry.name:

            sanitized_path = os.path.join(os.path.dirname(entry.path),
                                          entry.name.strip() + suffix)

            try:
                os.rename(entry.path, sanitized_path)
            except OSError as e:
                # dir not empty
                if e.errno is 39:
                    self.sanitize(entry, suffix + '_')
                else:
                    raise OSError(e)
            logging.debug('stripped dir: "%s" -> "%s"',
                          entry.path, sanitized_path)
            entry = pathlib.Path(sanitized_path)

        return entry
