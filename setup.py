# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.abspath(__file__))
long_desc = open(os.path.join(HERE, 'README.rst')).read()

requires = ['Sphinx>=0.6', 'Embedly']

setup(
    name='sphinxcontrib-embedly',
    version='0.2',
    url='http://github.com/jezdez/sphinxcontrib-embedly',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-embedly',
    license='BSD',
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    description='Sphinx "embedly" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
