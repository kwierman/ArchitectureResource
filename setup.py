#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import setup, find_packages
from pip.req import parse_requirements
import pip

install_reqs = reqs = [str(ir.req) for ir in parse_requirements('requirements.txt',
    session=pip.download.PipSession())]
dev_reqs = install_reqs

setup(
    name='architectureresource',
    version='0.1.0',
    description="These Violent Delights Have Violent Ends",
    long_description="""
        Some additional code was needed to fetch out resource usage information.
        Well, here it is.
    """,
    author="Kevin Wierman",
    author_email='kevin.wierman@pnnl.gov',
    url='https://github.com/kwierman/ArchitectureResource',
    packages=find_packages(),
    package_dir={'architectureresource':
                 'architectureresource'},
    entry_points={
        'console_scripts': [
            'architectureresource=architectureresource.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=reqs,
    license="MIT license",
    zip_safe=False,
    keywords='Neural Network Architecture Resource',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=dev_reqs
)
