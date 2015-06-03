import os
from setuptools import setup, find_packages


setup(
    name='keepassx',
    version='0.1.0',
    description="Python API and CLI for KeePassX",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.rst')).read(),
    author='James Saryerwinnie',
    author_email='js@jamesls.com',
    packages=find_packages(),
    keywords="keepassx",
    url="https://github.com/jamesls/python-keepassx",
    scripts=['bin/kp'],
    install_requires=[
        'pycrypto>=2.6.1,<3.0.0',
        'PyYAML>=3.10,<4.0.0',
        'prettytable==0.7.2',
        'six>=1.3.0,<2.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: '
        'GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Systems Administration',
    ],
)
