from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Impuestos Internos Helper',
    version='1.0.1',
    description=' Generador de codigo de control V7 para Impuestos Internos.',
    url='https://github.com/drkpkg/codigo_control',
    author='drkpkg',
    author_email='daniel.uremix@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='impuestos bolivia',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['qrcode'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
        'sample': ['casos.txt'],
    },
    data_files=[('data', ['data/lib/impuestos_internos.py'])],
)
