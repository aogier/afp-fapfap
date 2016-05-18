'''
Created on 18 mag 2016

@author: oggei
'''
import unittest
from tempfile import mkdtemp
import shutil
from afpfapfap.main import clean_dir
from pathlib import Path
from afpfapfap import logging

log = logging.get('tests')


class TestMain(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = mkdtemp()
        self.path = Path(self.tempdir)

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.tempdir)

    def testMainMethodDryRun(self):

        for d in [' dir', '  dir', '   dir']:
            path = self.path.joinpath(d)
            path.mkdir()
            path.joinpath(':2eDS_Store').touch()

        before = set(x.path for x in self.path.glob('**/*'))
        clean_dir(self.path, execute=False)
        after = set(x.path for x in self.path.glob('**/*'))

        self.assertEqual(before, after, 'no')
