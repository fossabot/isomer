"""
Hackerfleet Operating System - Backend

Module: Events
==============

Major HFOS event declarations

:copyright: (C) 2011-2015 riot@hackerfleet.org
:license: GPLv3 (See LICENSE)

"""

__author__ = "Heiko 'riot' Weinen <riot@hackerfleet.org>"

from circuits.core import Event

from hfos.logger import hfoslog, debug

# Clientmanager Events


class send(Event):
    """Send a packet to a known client by UUID"""

    def __init__(self, uuid, packet, *args):
        """

        :param uuid: Unique User ID of known connection
        :param packet: Data packet to transmit to client
        :param args: Further Args
        """
        super(send, self).__init__(*args)
        self.uuid = uuid
        self.packet = packet

        hfoslog("Send event generated:", uuid, packet, lvl=debug)


class broadcast(Event):
    """Send a packet to a known client by UUID"""

    def __init__(self, broadcasttype, content, *args):
        """

        :param uuid: Unique User ID of known connection
        :param packet: Data packet to transmit to client
        :param args: Further Args
        """
        super(broadcast, self).__init__(*args)
        self.broadcasttype = broadcasttype
        self.content = content

        hfoslog("Broadcast event generated:", broadcasttype, content, lvl=debug)


# Authenticator Events


class authenticationrequest(Event):
    """A client wants to authenticated a connection"""

    def __init__(self, username, passhash, uuid, sock, *args):
        """

        :param username: Account username
        :param passhash: Account md5 hash
        :param uuid: Unique User ID of known connection
        :param sock: Associated Socket
        :param args: Further Args
        """
        super(authenticationrequest, self).__init__(*args)

        self.username = username
        self.passhash = passhash
        self.sock = sock
        self.uuid = uuid


class authentication(Event):
    """Authentication has been granted to a client"""

    def __init__(self, username, userdata, clientuuid, useruuid, sock, *args):
        """

        :param username: Account username
        :param userdata: Tuple containing both useraccount and userprofile
        :param uuid: Unique User ID of known connection
        :param sock: Associated Socket
        :param args: Further Args
        """
        super(authentication, self).__init__(*args)

        self.username = username
        self.userdata = userdata
        self.clientuuid = clientuuid
        self.useruuid = useruuid
        self.sock = sock

        hfoslog("Authentication granted:", self.__dict__, lvl=debug)


class profileupdate(Event):
    """A user has changed his profile"""

    def __init__(self, profile, uuid, sock, *args):
        """

        :param profile: The new profile data
        :param uuid: Unique User ID of user account
        :param sock: Associated Socket
        :param args: Further Args
        """
        super(profileupdate, self).__init__(*args)

        self.profile = profile
        self.uuid = uuid
        self.sock = sock
        hfoslog(self.__dict__)


# Chat Events


class chatmessage(Event):
    """A new chat message has been received from a client"""

    def __init__(self, msg, sender, timestamp, *args):
        """

        :param msg: New message to be broadcast
        :param sender: Originating client object
        :param timestamp: Timestamp of server reception
        :param args: Further Args
        """
        super(chatmessage, self).__init__(*args)
        self.sender = sender
        self.timestamp = timestamp
        self.msg = msg

        hfoslog("CHAT: Message generated")


class chatevent(Event):
    """A new chat event has been generated by the client"""

    def __init__(self, sender, timestamp, content, *args):
        """

        :param msgtype: One of "Leave", "Join"
        :param sender: Originating client object
        :param timestamp: Timestamp of server reception
        :param args: Further Args
        """
        super(chatevent, self).__init__(*args)
        self.sender = sender
        self.timestamp = timestamp
        self.content = content

        hfoslog("CHAT: Event generated")


# Mapview Events


class mapviewrequest(Event):
    """A mapview request for an update or subscription management"""

    def __init__(self, sender, request, *args):
        """

        :param sender: Originating Client Object
        :param requesttype: One of "Update", "Subscribe", "Unsubscribe"
        :param mapview: The new mapview object
        :param args: Further Args
        """
        super(mapviewrequest, self).__init__(*args)
        self.sender = sender
        self.request = request

        hfoslog("MVS: Update-Event generated")


class mapviewbroadcast(Event):
    """A user changed his mapview and subscribers need to get notified"""

    def __init__(self, sender, mapview, *args):
        """

        :param sender: Originating User object
        :param mapview: New mapview update
        :param args: Further Args
        """
        super(mapviewbroadcast, self).__init__(*args)
        self.sender = sender
        self.mapview = mapview

        hfoslog("MVS: Broadcast-Event generated")


# Sensor Events


class sensordata(Event):
    """New sensordata has been parsed"""

    def __init__(self, data):
        """

        :param data: Parsed NMEA? Data
        """
        super(sensordata, self).__init__()
        self.data = data

