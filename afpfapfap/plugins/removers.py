'''
Created on 17 mag 2016

@author: oggei
'''
import re
from afpfapfap.main import NukedFile
from afpfapfap import logging

log = logging.get('cleaner')


class Remover(object):

    patterns = (
        re.compile(r'^:2eDS_Store$'),
    )

    def sanitize(self, entry, suffix='', execute=False):

        if any(pattern.match(entry.name)
               for pattern
               in self.patterns):
            if execute:
                entry.unlink()
            raise NukedFile('{0} removed')
