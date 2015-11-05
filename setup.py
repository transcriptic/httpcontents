from __future__ import print_function
from setuptools import setup
from os.path import join, dirname, abspath
import sys

long_description = ''

if 'upload' in sys.argv or '--long-description' in sys.argv:
    with open('README.rst') as f:
        long_description = f.read()

def main():
    reqs_file = join(dirname(abspath(__file__)), 'requirements.txt')
    with open(reqs_file) as f:
        requirements = [req.strip() for req in f.readlines()]

    setup(
        name='httpcontents',
        version='0.0.1',
        description="A Transcriptic LIMS-based ContentsManager for IPython.",
        long_description=long_description,
        author="Max Hodak",
        author_email="max@transcriptic.com",
        packages=[
            'httpcontents'
        ],
        license='MIT',
        include_package_data=True,
        zip_safe=False,
        url="https://github.com/transcriptic/httpcontents",
        install_requires=requirements
    )


if __name__ == '__main__':
    main()
