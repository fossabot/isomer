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

Test Isomer Basic Provisioning
============================



"""

from isomer.schemastore import build_schemastore_new


# from pprint import pprint


def test_invalid_schema_store_generation():
    """Tests for refusal of store generation with an invalid schema"""

    schemadefinition = {
        'foobar': 'qux'
    }

    schemastore = build_schemastore_new()

    # pprint(schemastore.keys())
