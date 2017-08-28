import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = ['stevedore',
                    ]

dependency_links = [
    'git+https://github.com/pexpect/pexpect@671417beb41c21f772687c565196fdde444b053b#egg=pexpect-3.3',
]

if os.environ.get('DEBUG'):
    install_requires += ['coverage==3.7.1',
                         ]

packages, package_data = [], {}

setup(
    name='ieo-afpfapfap',
    version='0.1',
    packages=packages,

    install_requires=install_requires,
    #     dependency_links=dependency_links,

    #     package_data=package_data,

    include_package_data=True,
    license='GPL',
    description='cleans up the mess that AFP services left on a migrated fileserver',
    url='https://github.com/aogier/afp-fapfap/',
    author='Alessandro Ogier',
    author_email='alessandro.ogier@gmail.com',
    classifiers=[
        'Programming Language :: Python',
    ],

    entry_points={
        'console_scripts': ['main = afpfapfap.main:run'],
        'fapfap.cleaners': [
            'whitespace trimmer = afpfapfap.plugins.renames:Renamer',
        ],
        'fapfap.removers': [
            'ds_store remover = afpfapfap.plugins.removers:Remover',
        ],

    },

    zip_safe=False,
)
