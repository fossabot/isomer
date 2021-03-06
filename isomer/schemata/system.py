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
Schema: System
==============

Contains
--------

System: Global systemwide settings


"""
from isomer.schemata.defaultform import savebutton, lookup_field
from isomer.schemata.base import base_object, uuid_object, language_field

SystemconfigSchema = base_object(
    "systemconfig", roles_read=["admin", "crew"], roles_write=["admin"]
)

SystemconfigSchema["properties"].update(
    {
        "active": {
            "type": "boolean",
            "title": "Active configuration",
            "description": "Determines which configuration will be used. "
            "Only one can be active.",
            "default": False,
        },
        "salt": {
            "type": "string",
            "minLength": 1,
            "title": "Salt",
            "description": "System hashing salt",
        },
        "description": {
            "type": "string",
            "format": "html",
            "title": "Description",
            "description": "System description",
        },
        "contact": {
            "type": "string",
            "title": "Contact",
            "description": "Contact e-mail address",
        },
        "language": language_field(),
        # TODO: This should probably be an extension of a future themes pack
        "defaulttheme": {
            "type": "string",
            "title": "Default new client theme",
            "description": "Default theme used for user " "interface",
        },
        "initial_state": {
            "type": "string",
            "title": "State after login",
            "description": "Frontend state, users are directed to after logging in.",
            "default": "",
        },
        "initial_state_args": {
            "type": "string",
            "title": "State arguments",
            "description": "Arguments (JSON) for login state.",
            "default": "",
        },
        "hostname": {
            "type": "string",
            "title": "Public hostname",
            "description": "Public FQDN hostname to use for internet "
            "based services (host.domain.tld)",
            "default": "localhost",
        },
        "modules": {"type": "object", "default": {}},
        "packages": {
            "type": "array",
            "default": [],
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                },
            },
        },
        "provisions": {
            "type": "object",
            "default": {"packages": []},
            "properties": {
                "packages": {
                    "type": "array",
                    "default": [],
                    "items": {"type": "string"},
                }
            },
        },
    }
)

SystemconfigForm = [
    {
        "type": "section",
        "htmlClass": "row",
        "items": [
            {
                "type": "section",
                "htmlClass": "col-xs-4",
                "items": ["name", "hostname", "language"],
            },
            {
                "type": "section",
                "htmlClass": "col-xs-4",
                "items": [{"key": "active", "readonly": True}, "contact"],
            },
            {
                "type": "section",
                "htmlClass": "col-xs-4",
                "items": ["initial_state", "initial_state_args"],
            },
        ],
    },
    {
        "id": "modules",
        "type": "section",
        "htmlClass": "row",
        "items": [
            {"type": "help", "helpvalue": "<h2>Default module configurations</h2>"}
        ],
    },
    "description",
    savebutton,
]

SystemconfigOptions = {"hidden": ["salt"]}

Systemconfig = {
    "schema": SystemconfigSchema,
    "form": SystemconfigForm,
    "options": SystemconfigOptions,
}
