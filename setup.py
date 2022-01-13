import os
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()



def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


if __name__ == '__main__':
    from distutils.core import setup

    extra_files = package_files('DesOptPy')
    setup(
        name='DesOptPy',
        version='2022.1.3',
        description='DESign OPTimization in PYthon',
        author='E. J. Wehrle',
        author_email='Erich.Wehrle@unibz.it',
        copyright='Copyright 2015-2022 E. J. Wehrle',
        package_data={'': extra_files},
        license='GNU Lesser General Public License 3.0',
        url='https://github.com/e-dub/DesOptPy',
        packages=['DesOptPy'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    )
