"""


Package: Provisions
===================

Initial client configuration data.
This contains tilelayer urls, api stuff etc.

:copyright: (C) 2011-2019 Heiko 'riot' Weinen@c-base.org
:license: AGPLv3 (See LICENSE)

"""

from isomer.logger import isolog, debug, warn  # , verbose, error, warn
from pkg_resources import iter_entry_points

__author__ = "Heiko 'riot' Weinen <riot@c-base.org>"


# TODO: This probably has to be moved somewhere else (due to clashes with namespace-architecture)
def build_provision_store():
    available = {}

    for provision_entrypoint in iter_entry_points(group="isomer.provisions", name=None):
        isolog("Provisions found: ", provision_entrypoint.name, lvl=debug, emitter="DB")
        try:
            available[provision_entrypoint.name] = provision_entrypoint.load()
        except ImportError:
            isolog(
                "Problematic provision: ",
                provision_entrypoint.name,
                exc=True,
                lvl=warn,
                emitter="PROVISIONS",
                frame_ref=2,
            )

    isolog("Found provisions: ", sorted(list(available.keys())), emitter="PROVISIONS")
    # pprint(available)

    return available


__import__("pkg_resources").declare_namespace(__name__)
