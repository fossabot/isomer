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

"""
Hackerfleet Operating System - Backend

Test Isomer Maintenance
=====================



"""

from circuits import Manager
import pytest
from isomer.database.components import Maintenance
import isomer.logger as logger

m = Manager()


def test_instantiate():
    """Tests correct instantiation"""
    maint = Maintenance()
    maint.register(m)

    assert type(maint) == Maintenance


def test_maintenance_log():
    log = logger.LiveLog
    logger.live = True

    maint = Maintenance()
    maint.register(m)

    pytest.clean_test_components()

    assert "Performing maintenance check" in str(log)
