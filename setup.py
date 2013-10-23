import os
import sys

from setuptools import setup, find_packages

sys.path.append('.')
from irianas_server import metadata


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

list_ssl = ['ssl-demo/' + item for item in os.listdir('ssl-demo')]

if 'VIRTUAL_ENV' in os.environ:
    path = os.path.join(os.environ['VIRTUAL_ENV'], 'ssl-demo')
else:
    path = '/etc/ssl/certs/'

data_ssl = {'data_files': [(path, list_ssl)]}

# define install_requires for specific Python versions
python_version_specific_requires = []

# as of Python >= 2.7 and >= 3.2, the argparse module is maintained within
# the Python standard library, otherwise we install it as a separate package
if sys.version_info < (2, 7) or (3, 0) <= sys.version_info < (3, 3):
    python_version_specific_requires.append('argparse')


# See here for more options:
# <http://pythonhosted.org/setuptools/setuptools.html>
setup_dict = dict(
    name=metadata.package,
    version=metadata.version,
    author=metadata.authors[0],
    author_email=metadata.emails[0],
    maintainer=metadata.authors[0],
    maintainer_email=metadata.emails[0],
    url=metadata.url,
    description=metadata.description,
    long_description=read('README.rst'),
    download_url=metadata.url,
    # Find a list of classifiers here:
    # <http://pypi.python.org/pypi?%3Aaction=list_classifiers>
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
    ],
    packages=find_packages(),
    install_requires=[
        # your module dependencies
    ] + python_version_specific_requires,
    zip_safe=False,  # don't use eggs
    entry_points={
        'console_scripts': [
            'irianas_server_cli = irianas_server.main:entry_point'
        ],
        # if you have a gui, use this
        # 'gui_scripts': [
        #     'irianas_server_gui = irianas_server.gui:entry_point'
        # ]
    },
    **data_ssl
)


def main():
    setup(**setup_dict)


if __name__ == '__main__':
    main()
