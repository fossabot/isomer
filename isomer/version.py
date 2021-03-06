#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Isomer - The distributed application framework
# ==============================================
# Copyright (C) 2011-2019 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Version Module

Unified Isomer wide version number.
"""

from isomer.logger import isolog, error

try:
    from isomer.scm_version import version

    version_info = version
except ImportError as e:
    isolog("Could not import scm version:", e, lvl=error)
    version_info = (1, 2, 1, "dev")  # (major, minor, patch, dev?)
    version = ".".join(map(str, version_info)) if version_info[-1] != "dev" else "dev"
