from setuptools import setup, find_packages


setup(
    name='Rocamgo',
    version=0.2,
    description='Rocamgo is recogniter of the go games by processing digital images with opencv',
    long_description='Rocamgo is recogniter of the go games by processing digital images with opencv extended',
    author='Victor Ramirez de la Corte',
    author_email='virako.9@gmail.com',
    url='https://github.com/virako/Rocamgo-ng',
    download_url='https://github.com/Virako/Rocamgo-ng/archive/master.zip',
    license='GPLv3',
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Spanglish',
        'Operating System :: Linux',
        'Programming Language :: Python',
        ],
    )
