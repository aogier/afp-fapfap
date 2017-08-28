'''
Created on 28/gen/2016

@author: oggei
'''
import unittest
from tempfile import mkdtemp
import shutil
from afpfapfap.main import clean_dir
from pathlib import Path
from afpfapfap import logging

log = logging.get('tests')


class TestWhitespace(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = mkdtemp()
        self.path = Path(self.tempdir)

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.tempdir)

    def testLeadingWhitespaceRemoval(self):

        self.path.joinpath(' dir').mkdir()

        clean_dir(self.path, execute=True)

        self.assertTrue(
            self.path.joinpath('dir').exists(),
            'leading space not removed: %s' % [x for x
                                               in self.path.iterdir()])

    def testTrailingWhitespaceRemoval(self):

        self.path.joinpath('dir ').mkdir()

        clean_dir(self.path, execute=True)

        self.assertTrue(
            self.path.joinpath('dir').exists(),
            'trailing space not removed: %s' % [x for x
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
                         len(list(self.path.glob('**/*'))),
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
                         len(list(self.path.glob('**/*'))),
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

        self.assertEqual(set(x for x in self.path.iterdir()),
                         set(self.path.joinpath(x)
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

        self.assertEqual(set(x for x in self.path.iterdir()),
                         set(self.path.joinpath(x)
                             for x in ['dir', 'dir_', 'dir__']),
                         'no')


class TestSlashes(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = mkdtemp()
        self.path = Path(self.tempdir)

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.tempdir)

    def testSlashRemoval(self):

        self.path.joinpath('di:2fr').mkdir()

        clean_dir(self.path, execute=True)

        self.assertTrue(
            self.path.joinpath('di_r').exists(),
            'slash not removed: %s' % [x for x
                                       in self.path.iterdir()])

    def testDoubleSlashRemovalOnEmptyDir(self):
        '''
        We have a directory with multiple empty 
        subdirectories whose name differs only for 
        different leading whitespaces:

         * base
           * 'd:2fir'
           * 'd:2fir '

        Resulting tree must be:

         * base
           * d_ir
        '''

        for d in ['d:2fir', 'd:2fir ']:
            self.path.joinpath(d).mkdir()

        clean_dir(self.path, execute=True)

        self.assertEqual(1,
                         len(list(self.path.glob('**/*'))),
                         'no')

        self.assertEqual(set(self.path.glob('**/*')),
                         set([self.path.joinpath('d_ir')]),
                         'no')


class TestDots(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = mkdtemp()
        self.path = Path(self.tempdir)

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.tempdir)

    def testDotRemoval(self):

        self.path.joinpath('di:2er').mkdir()

        clean_dir(self.path, execute=True)

        self.assertTrue(
            self.path.joinpath('di.r').exists(),
            'dot not removed: %s' % [x for x
                                     in self.path.iterdir()])

    def testDoubleDotRemovalOnEmptyDir(self):
        '''
        We have a directory with multiple empty 
        subdirectories whose name differs only for 
        different leading whitespaces:

         * base
           * 'd:2eir'
           * 'd:2eir '

        Resulting tree must be:

         * base
           * d.ir
        '''

        for d in ['d:2eir', 'd:2eir ']:
            self.path.joinpath(d).mkdir()

        clean_dir(self.path, execute=True)

        self.assertEqual(1,
                         len(list(self.path.glob('**/*'))),
                         'no')

        self.assertEqual(set(self.path.glob('**/*')),
                         set([self.path.joinpath('d.ir')]),
                         'no')

    def testDoubleDotRemoval(self):
        '''
        We have a directory with multiple empty 
        subdirectories whose name differs only for 
        different leading whitespaces:

         * base
           * ':2edir/file'
           * '.dir /file'

        Resulting tree must be:

         * base
           * .dir/file
           * .dir_/file
        '''

        for d in [':2edir', '.dir']:
            p = self.path.joinpath(d)
            p.mkdir()
            p.joinpath('file').touch()

        clean_dir(self.path, execute=True)

        self.assertEqual(4,
                         len(list(self.path.glob('**/*'))),
                         'no')

        self.assertEqual(set(self.path.glob('**/*')),
                         set([self.path.joinpath('.dir'),
                              self.path.joinpath('.dir').joinpath('file'),
                              self.path.joinpath('.dir_'),
                              self.path.joinpath('.dir_').joinpath('file')
                              ]),
                         'no')
