import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
]

dependency_links = [
    'git+https://github.com/pexpect/pexpect@671417beb41c21f772687c565196fdde444b053b#egg=pexpect-3.3',
]

if os.environ.get('DEBUG'):
    install_requires += ['ipython',
                         'coverage==3.7.1',
                         ]

# package_dir = 'pancreatic_cancer'


# def fullsplit(path, result=None):
#     """
#     Split a pathname into components (the opposite of os.path.join) in a
#     platform-neutral way.
#     """
#     if result is None:
#         result = []
#     head, tail = os.path.split(path)
#     if head == '':
#         return [tail] + result
#     if head == path:
#         return result
#     return fullsplit(head, [tail] + result)

packages, package_data = [], {}

# for dirpath, dirnames, filenames in os.walk(package_dir):
#     # Ignore PEP 3147 cache dirs and those whose names start with '.'
#     dirnames[:] = [
#         d for d in dirnames if not d.startswith('.') and d != '__pycache__']
#     parts = fullsplit(dirpath)
#     package_name = '.'.join(parts)
#     if '__init__.py' in filenames:
#         packages.append(package_name)
#     elif filenames:
#         relative_path = []
#         while '.'.join(parts) not in packages:
#             relative_path.append(parts.pop())
#         relative_path.reverse()
#         path = os.path.join(*relative_path)
#         package_files = package_data.setdefault('.'.join(parts), [])
#         package_files.extend([os.path.join(path, f) for f in filenames])


setup(
    name='ieo-afpfapfap',
    version='0.1',
    packages=packages,

    install_requires=install_requires,
    #     dependency_links=dependency_links,

    #     package_data=package_data,

    include_package_data=True,
    license='Proprietary',  # example license
    description='A Django-based database for a pancreatic actionability database',
    url='http://www.ieo.eu/',
    author='Alessandro Ogier',
    author_email='alessandro.ogier@ieo.eu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3 :: Only',
    ],

    entry_points={
        'console_scripts': ['main = afpfapfap.main:run']
    },
)
