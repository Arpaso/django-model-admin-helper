# -*- coding: utf-8 -*-
"""
Configuration file used by setuptools. It creates 'egg', install all dependencies.
"""

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#Dependencies - python eggs
install_requires = [
        'setuptools',
        'Django',
]

#Execute function to handle setuptools functionality
setup(name="django-model-admin-helper",
    version="0.2",
    description="Admin helpers",
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    py_modules = ['admin_helpers'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    author='Arpaso',
    author_email='arvid@arpaso.com',
    url='http://github.com/Arpaso/django-model-admin-helper',
    download_url='http://github.com/Arpaso/django-model-admin-helper/tarball/0.1',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ),
)
