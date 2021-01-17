from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

HERE_PATH = path.abspath(path.dirname(__file__))

with open(path.join(HERE_PATH, 'README.md')) as readme_fd:
    LONG_DESCRIPTION = readme_fd.read()

setup(
    name='pik-address-formatter',
    version='1.1',
    author='pik-software',
    author_email='no-reply@pik-software.ru',
    description='Address formatter for address components from housing',
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/pik-software/pik-address-formatter.git',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='apiqa',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],
    python_requires='~=3.6',
)
