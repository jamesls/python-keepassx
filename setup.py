import os
from setuptools import setup, find_packages


setup(
    name='keepassx',
    version='0.0.1',
    description="Python API and CLI for KeePassX",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.rst')).read(),
    license='BSD',
    author='James Saryerwinnie',
    author_email='js@jamesls.com',
    packages=find_packages(),
    keywords="keepassx",
    url="https://github.com/jamesls/keepassx",
    scripts=['bin/kp'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
    ],
    install_requires=[
        'pycrypto==2.6',
        'PyYAML==3.10',
    ]
)


