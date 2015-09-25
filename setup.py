"""
setup.py

The latest version of this package is available at:
<https://github.com/jantman/archautorepo>

##################################################################################
Copyright 2015 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of archautorepo, also known as arch-autorepo.

    archautorepo is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    archautorepo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with archautorepo.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
##################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/archautorepo> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
##################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################
"""

from setuptools import setup, find_packages
from sys import version_info
from archautorepo.version import _VERSION, _PROJECT_URL

with open('README.rst') as file:
    long_description = file.read()

requires = [
]

classifiers = [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Build Tools',
    'Topic :: System :: Installation/Setup',
    'Topic :: System :: Operating System',
    'Topic :: System :: Software Distribution',
    'Topic :: Utilities'
]

setup(
    name='archautorepo',
    version=_VERSION,
    author='Jason Antman',
    author_email='jason@jasonantman.com',
    packages=find_packages(),
    #entry_points="""
    #[console_scripts]
    #archautorepo = archautorepo.runner:console_entry_point
    #""",
    url=_PROJECT_URL,
    description='Automatic Arch Linux package rebuilds and repository creation.',
    long_description=long_description,
    install_requires=requires,
    keywords="archlinux arch pacman package rebuild repository",
    classifiers=classifiers
)
