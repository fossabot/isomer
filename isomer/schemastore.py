from copy import deepcopy
from pkg_resources import iter_entry_points, DistributionNotFound

import formal
import jsonschema

from isomer.logger import isolog, verbose, warn, debug
from isomer.misc import all_languages, i18n as _


def schemata_log(*args, **kwargs):
    """Log as emitter 'SCHEMATA'"""
    kwargs.update({"emitter": "SCHEMATA", "frame_ref": 2})
    isolog(*args, **kwargs)


schemastore = None
l10n_schemastore = {}
configschemastore = {}


def build_schemastore_new():
    available = {}

    for schema_entrypoint in iter_entry_points(group="isomer.schemata", name=None):
        try:
            schemata_log("Schemata found: ", schema_entrypoint.name, lvl=verbose)
            schema = schema_entrypoint.load()
            available[schema_entrypoint.name] = schema
        except (ImportError, DistributionNotFound) as e:
            schemata_log(
                "Problematic schema: ", schema_entrypoint.name, exc=True, lvl=warn
            )

    def schema_insert(dictionary, path, obj):
        path = path.split("/")

        place = dictionary

        for element in path:
            if element != "":
                place = place[element]

        place.update(obj)

        return dictionary

    def form_insert(form, index, path, obj):
        path = path.split("/")
        place = None
        if isinstance(index, str):
            for widget in form:
                if isinstance(widget, dict) and widget.get("id", None) is not None:
                    place = widget
        else:
            place = form[index]

        if place is None:
            schemata_log("No place to insert into form found:", path, form, obj)
            return

        for element in path:
            schemata_log(element, place, lvl=verbose)
            try:
                element = int(element)
            except ValueError:
                pass
            if element != "":
                place = place[element]

        if isinstance(place, dict):
            place.update(obj)
        else:
            place.append(obj)

        return form

    for key, item in available.items():
        extends = item.get("extends", None)
        if extends is not None:
            schemata_log(key, "extends:", extends, pretty=True, lvl=verbose)

            for model, extension_group in extends.items():
                schema_extensions = extension_group.get("schema", None)
                form_extensions = extension_group.get("form", None)
                schema = available[model].get("schema", None)
                form = available[model].get("form", None)

                original_schema = deepcopy(schema)

                if schema_extensions is not None:
                    schemata_log("Extending schema", model, "from", key, lvl=debug)
                    for path, extensions in schema_extensions.items():
                        schemata_log(
                            "Item:", path, "Extensions:", extensions, lvl=verbose
                        )
                        for obj in extensions:
                            available[model]["schema"] = schema_insert(
                                schema, path, obj
                            )
                            schemata_log("Path:", path, "obj:", obj, lvl=verbose)

                if form_extensions is not None:
                    schemata_log("Extending form of", model, "with", key, lvl=verbose)
                    for index, extensions in form_extensions.items():
                        schemata_log(
                            "Item:", index, "Extensions:", extensions, lvl=verbose
                        )
                        for path, obj in extensions.items():
                            if not isinstance(obj, list):
                                obj = [obj]
                            for thing in obj:
                                available[model]["form"] = form_insert(
                                    form, index, path, thing
                                )
                                schemata_log("Path:", path, "obj:", thing, lvl=verbose)

                # schemata_log(available[model]['form'], pretty=True, lvl=warn)
                try:
                    jsonschema.Draft4Validator.check_schema(schema)
                except jsonschema.SchemaError as e:
                    schemata_log(
                        "Schema extension failed:", model, extension_group, exc=True
                    )
                    available[model]["schema"] = original_schema

    schemata_log(
        "Found", len(available), "schemata: ", sorted(available.keys()), lvl=debug
    )

    return available


def build_l10n_schemastore(available):
    l10n_schemata = {}

    for lang in all_languages():

        language_schemata = {}

        def translate(schema):
            """Generate a translated copy of a schema"""

            localized = deepcopy(schema)

            def walk(branch):
                """Inspect a schema recursively to translate descriptions and titles"""

                if isinstance(branch, dict):

                    if "title" in branch and isinstance(branch["title"], str):
                        # schemata_log(branch['title'])
                        branch["title"] = _(branch["title"], lang=lang)
                    if "description" in branch and isinstance(
                        branch["description"], str
                    ):
                        # schemata_log(branch['description'])
                        branch["description"] = _(branch["description"], lang=lang)

                    for key, item in branch.items():
                        walk(item)

            walk(localized)

            return localized

        for key, item in available.items():
            language_schemata[key] = translate(item)

        l10n_schemata[lang] = language_schemata

        # schemata_log(l10n_schemata['de']['client'], pretty=True, lvl=error)

    return l10n_schemata


def test_schemata():
    """Validates all registered schemata"""

    objects = {}

    for schemaname in schemastore.keys():
        objects[schemaname] = formal.model_factory(schemastore[schemaname]["schema"])
        try:
            testobject = objects[schemaname]()
            testobject.validate()
        except Exception as e:
            schemata_log("Blank schema did not validate:", schemaname, exc=True)

            # pprint(objects)
