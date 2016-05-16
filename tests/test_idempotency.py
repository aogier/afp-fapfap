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

                print ('made temp dir:', temp_child)

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

            print('touched -%s-' % temp_file)
            yield temp_file

        return 1

    def testIdempotency(self):
        a = set(x for x
                in self.populate(self.tempdir, depth=2, width=2))

        b = set(x.path for x
                in self.path.iterdir())

        c = set(x.path for x
                in self.path.iterdir())

        self.assertEqual(b, c, 'no')

        print('\n\ncane\n')
