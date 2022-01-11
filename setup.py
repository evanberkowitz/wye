#   wye
#   tee, but produces graphs via matplotlib
#   Copyright (C) 2021 Evan Berkowitz
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from distutils.core import setup


setup(
    name='wye',
    description='Tee but make graphs.',
    author='Evan Berkowitz',
    author_email='git@evanberkowitz.com',

    # pip:
    scripts=['bin/wye',],
    requires=['matplotlib', 'fileinput', 'numpy', 'argparse', 'itertools'],

    license='GPLv3+',
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        ]
)
