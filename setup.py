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
    version="0.1",
    description="Admin helpers",
    long_description=read('README'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    author='Arpaso',
    author_email='arvid@arpaso.com',
    url='http://github.com/Arpaso/django-model-admin-helper.git',
    classifiers=(
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ),
)

