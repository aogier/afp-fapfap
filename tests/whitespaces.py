'''
Created on 28/gen/2016

@author: oggei
'''
import unittest
from pkg_resources import Requirement, resource_filename  # @UnresolvedImport
from tempfile import mkdtemp
import os
import shutil


class TestWhitespace(unittest.TestCase):

    def setUp(self):
        super.setUp()
        self.tempdir = mkdtemp()

    def tearDown(self):
        super.tearDown()
        shutil.rmtree(self.tempdir)

    def testLeadingWhitespaceRemoval(self):

        os.mkdir(os.path.join(self.tempdir, ' dir'))

        self.assertTrue(
            os.path.exists(os.path.join(self.tempdir, 'dir')),
            'leading space not removed')
