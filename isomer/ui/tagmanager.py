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
from isomer.events.system import authorized_event

"""

Module: TagManager
==================


"""

from circuits import Timer, Event

from isomer.events.client import send
from isomer.component import ConfigurableComponent
from isomer.database import objectmodels
from isomer.logger import warn, debug, verbose  # , error, hilight
from isomer.component import handler


class get_tagged(authorized_event):
    pass


class TagManager(ConfigurableComponent):
    """
    Various tag related operations.
    """

    channel = "isomer-web"

    configprops = {}

    def __init__(self, *args):
        super(TagManager, self).__init__("TM", *args)

        self.tags = {}

        tag = objectmodels["tag"]

        for item in tag.find():
            self.tags[item.name.upper()] = item

        self.log("Tags:", list(self.tags.keys()), pretty=True, lvl=verbose)

        # tagged = self._get_tagged('PR')

        # for item in tagged:
        #    self.log("Found tagged items:", item.serializablefields(), pretty=True)
        # Timer(3, Event.create('getTagged', 'PR')).register(self)

    # @handler('getTagged')
    def _get_tagged(self, tag):
        tag = self.tags[tag]
        self.log("TAG UUID", tag.uuid)
        tagged = []
        for model in objectmodels.values():
            self.log(model, pretty=True)
            self.log("Find:", model.find, pretty=True)
            for item in model.find({"tags": {"$in": [tag.uuid]}}):
                tagged.append(item.serializablefields())

        return tagged

    @handler(get_tagged)
    def get_tagged(self, event):
        """Return a list of tagged objects for a schema"""
        self.log(
            "Tagged objects request for", event.data, "from", event.user, lvl=debug
        )
        if event.data.upper() in self.tags:
            tagged = self._get_tagged(event.data.upper())

            response = {
                "component": "isomer.ui.tagmanager",
                "action": "get_tagged",
                "data": tagged,
            }
            self.fireEvent(send(event.client.uuid, response))
        else:
            self.log("Unavailable schema requested!", lvl=warn)
