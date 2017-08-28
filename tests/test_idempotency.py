'''
Created on 02/feb/2016

@author: oggei
'''
import os
from pathlib import Path
import shutil
from tempfile import mkdtemp, mkstemp
import unittest
from random import random
from afpfapfap.main import clean_dir
from afpfapfap import logging

log = logging.get('tests')


class TestIdempotency(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = mkdtemp()
        self.path = Path(self.tempdir)

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.tempdir)

    def populate(self, tempdir, depth=3, width=3):

        temp_file = None
        temp_child = None
        for i in range(width):

            if depth:
                if random() < 0.5 or not temp_child:
                    temp_child = mkdtemp(dir=tempdir)
                else:
                    temp_child += ' '
                    os.mkdir(temp_child)

                log.debug('made temp dir: %s', temp_child)

                yield from self.populate(tempdir=temp_child,
                                         depth=depth - 1)
                yield temp_child

            if random() < 0.5 or not temp_file:
                fd, temp_file = mkstemp(dir=tempdir)
                f = os.fdopen(fd, 'w')
                f.close()
            else:
                temp_file += ' '
                open(temp_file, 'w').close()

            log.debug('touched -%s-', temp_file)
            yield temp_file

        return 1

    def testIdempotency(self):
        a = set(x for x
                in self.populate(self.tempdir, depth=3, width=3))

        clean_dir(self.path, execute=True)
        b = set(x for x
                in self.path.glob('**/*'))

        clean_dir(self.path, execute=True)
        c = set(x for x
                in self.path.glob('**/*'))

        self.assertNotEqual(a, b, 'no')
        self.assertEqual(b, c, 'no')
