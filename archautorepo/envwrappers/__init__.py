"""
archautorepo/envwrappers/__init__.py

The latest version of this package is available at:
<https://github.com/jantman/archautorepo>

################################################################################
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
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/archautorepo> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import abc

class EnvWrapper(object):
    """
    ArchAutoRepo uses environment wrappers (EnvWrappers) to wrap all interaction
    with the build environment, whether it is a Docker container, the local
    system, or something new in the future (like a cloud instance). EnvWrappers
    specify how to run the actual commands, as well as how to setup and tear
    down the build environment. In addition, they provide context managers to
    ensure that the build environment is properly torn down.

    The EnvWrapper metaclass specifies the interface to be implemented by all
    EnvWrapper types, by using Python's
    `abc <https://docs.python.org/2/library/abc.html>`_ abstract base class
    functionality.

    All EnvWrapper classes should be of type EnvWrapper.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    # context manager(s)?
    # https://docs.python.org/2/library/contextlib.html
    # https://www.python.org/dev/peps/pep-0343/
    
