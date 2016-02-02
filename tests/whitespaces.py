'''
Created on 28/gen/2016

@author: oggei
'''
import unittest
from pkg_resources import Requirement, resource_filename  # @UnresolvedImport
from tempfile import mkdtemp
import os
import shutil
from afpfapfap.main import scandirs
from pathlib import Path


class TestWhitespace(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = mkdtemp()
        self.path = Path(self.tempdir)

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.tempdir)

    def testLeadingWhitespaceRemoval(self):

        path = os.path.join(self.tempdir, ' dir')
        normalized_path = os.path.join(self.tempdir, 'dir')

        os.mkdir(path)
        for entry in scandirs(Path(self.tempdir)):
            pass

        self.assertTrue(
            os.path.exists(normalized_path),
            'leading space not removed: %s' % [x.path for x
                                               in os.scandir(self.tempdir)])

    def testTrailingWhitespaceRemoval(self):

        path = os.path.join(self.tempdir, 'dir ')
        normalized_path = os.path.join(self.tempdir, 'dir')

        os.mkdir(path)
        for entry in scandirs(Path(self.tempdir)):
            pass

        self.assertTrue(
            os.path.exists(normalized_path),
            'trailing space not removed: %s' % [x.path for x
                                                in os.scandir(self.tempdir)])

    def testDoubleLeadingWhitespaceRemovalOnEmptyDir(self):

        for d in [' dir', '  dir']:
            os.mkdir(os.path.join(self.tempdir, d))

        for _entry in scandirs(self.path):
            pass

        self.assertEqual(1,
                         len(list(self.path.iterdir())),
                         'no')

    def testDoubleLeadingWhitespaceRemoval(self):

        os.mkdir(os.path.join(self.tempdir, ' dir'))
        os.mkdir(os.path.join(self.tempdir, '  dir'))

        open(os.path.join(self.tempdir, ' dir', 'file'), 'w').close()
        open(os.path.join(self.tempdir, '  dir', 'file'), 'w').close()

        for _entry in scandirs(self.path):
            pass

        self.assertEqual(2,
                         len(list(self.path.iterdir())),
                         'no')
