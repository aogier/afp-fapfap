'''
Created on 28/gen/2016

@author: oggei
'''
import unittest
from pkg_resources import Requirement, resource_filename  # @UnresolvedImport
from tempfile import mkdtemp
import os
import shutil
from afpfapfap.main import clean_dir
from pathlib import Path


class TestWhitespace(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = mkdtemp()
        self.path = Path(self.tempdir)

    def tearDown(self):
        print('CANENE')
        super().tearDown()
        shutil.rmtree(self.tempdir)

    def testLeadingWhitespaceRemoval(self):

        self.path.joinpath(' dir').mkdir()

        clean_dir(self.path, execute=True)

        self.assertTrue(
            self.path.joinpath('dir').exists(),
            'leading space not removed: %s' % [x.path for x
                                               in self.path.iterdir()])

    def testTrailingWhitespaceRemoval(self):

        self.path.joinpath('dir ').mkdir()

        clean_dir(self.path, execute=True)

        self.assertTrue(
            self.path.joinpath('dir').exists(),
            'trailing space not removed: %s' % [x.path for x
                                                in self.path.iterdir()])

    def testDoubleLeadingWhitespaceRemovalOnEmptyDir(self):
        '''
        We have a directory with multiple empty 
        subdirectories whose name differs only for 
        different leading whitespaces:

         * base
           * ' dir'
           * '  dir'

        Resulting tree must be:

         * base
           * dir
        '''

        for d in [' dir', '  dir']:
            self.path.joinpath(d).mkdir()

        clean_dir(self.path, execute=True)

        self.assertEqual(1,
                         len(list(self.path.iterdir())),
                         'no')

    def testDoubleTrailingWhitespaceRemovalOnEmptyDir(self):
        '''
        We have a directory with multiple empty 
        subdirectories whose name differs only for 
        different trailing whitespaces:

         * base
           * 'dir '
           * 'dir  '

        Resulting tree must be:

         * base
           * dir
        '''

        for d in ['dir ', 'dir  ']:
            self.path.joinpath(d).mkdir()

        clean_dir(self.path, execute=True)

        self.assertEqual(1,
                         len(list(self.path.iterdir())),
                         'no')

    def testMultipleLeadingWhitespaceRemoval(self):
        '''
        We have a directory with multiple non-empty 
        subdirectories whose name differs only for 
        different leading whitespaces:

         * base
           * ' dir'
           * '  dir'
           * '   dir'

        Resulting tree must be:

         * base
           * dir
           * dir_
           * dir__ 
        '''

        for d in [' dir', '  dir', '   dir']:
            path = self.path.joinpath(d)
            path.mkdir()
            path.joinpath('file').touch()

        clean_dir(self.path, execute=True)

        self.assertEqual(3,
                         len(list(self.path.iterdir())),
                         'no')

        self.assertEqual(set(x.path for x in self.path.iterdir()),
                         set(self.path.joinpath(x).path
                             for x in ['dir', 'dir_', 'dir__']),
                         'no')

    def testMultipleTrailingWhitespaceRemoval(self):
        '''
        We have a directory with multiple non-empty 
        subdirectories whose name differs only for 
        different trailing whitespaces:

         * base
           * 'dir '
           * 'dir  '
           * 'dir   '

        Resulting tree must be:

         * base
           * dir
           * dir_
           * dir__ 
        '''

        for d in ['dir ', 'dir  ', 'dir   ']:
            path = self.path.joinpath(d)
            path.mkdir()
            path.joinpath('file').touch()

        clean_dir(self.path, execute=True)

        self.assertEqual(3,
                         len(list(self.path.iterdir())),
                         'no')

        self.assertEqual(set(x.path for x in self.path.iterdir()),
                         set(self.path.joinpath(x).path
                             for x in ['dir', 'dir_', 'dir__']),
                         'no')
