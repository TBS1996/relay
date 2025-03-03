from __future__ import annotations

import json

from sentry_relay._lowlevel import lib, ffi
from sentry_relay.utils import (
    encode_str,
    decode_str,
    rustcall,
    RustObject,
    attached_refs,
    make_buf,
)


__all__ = [
    "split_chunks",
    "meta_with_chunks",
    "StoreNormalizer",
    "GeoIpLookup",
    "is_glob_match",
    "is_codeowners_path_match",
    "parse_release",
    "validate_pii_config",
    "convert_datascrubbing_config",
    "pii_strip_event",
    "pii_selector_suggestions_from_event",
    "VALID_PLATFORMS",
    "validate_sampling_condition",
    "validate_sampling_configuration",
    "validate_project_config",
    "normalize_global_config",
    "run_dynamic_sampling",
]


def _init_valid_platforms() -> frozenset[str]:
    size_out = ffi.new("uintptr_t *")
    strings = rustcall(lib.relay_valid_platforms, size_out)

    valid_platforms = []
    for i in range(int(size_out[0])):
        valid_platforms.append(decode_str(strings[i], free=True))

    return frozenset(valid_platforms)


VALID_PLATFORMS = _init_valid_platforms()


def split_chunks(string, remarks):
    json_chunks = rustcall(
        lib.relay_split_chunks,
        encode_str(string),
        encode_str(json.dumps(remarks)),
    )
    return json.loads(decode_str(json_chunks, free=True))


def meta_with_chunks(data, meta):
    if not isinstance(meta, dict):
        return meta

    result = {}
    for key, item in meta.items():
        if key == "" and isinstance(item, dict):
            result[""] = item.copy()
            if item.get("rem") and isinstance(data, str):
                result[""]["chunks"] = split_chunks(data, item["rem"])
        elif isinstance(data, dict):
            result[key] = meta_with_chunks(data.get(key), item)
        elif isinstance(data, list):
            int_key = int(key)
            val = data[int_key] if int_key < len(data) else None
            result[key] = meta_with_chunks(val, item)
        else:
            result[key] = item

    return result


class GeoIpLookup(RustObject):
    __dealloc_func__ = lib.relay_geoip_lookup_free
    __slots__ = ("_path",)

    @classmethod
    def from_path(cls, path):
        if isinstance(path, str):
            path = path.encode("utf-8")
        rv = cls._from_objptr(rustcall(lib.relay_geoip_lookup_new, path))
        rv._path = path
        return rv

    def __repr__(self):
        return f"<GeoIpLookup {self._path!r}>"


class StoreNormalizer(RustObject):
    __dealloc_func__ = lib.relay_store_normalizer_free
    __init__ = object.__init__
    __slots__ = ("__weakref__",)

    def __new__(cls, geoip_lookup=None, **config):
        config = json.dumps(config)
        geoptr = geoip_lookup._get_objptr() if geoip_lookup is not None else ffi.NULL
        rv = cls._from_objptr(
            rustcall(lib.relay_store_normalizer_new, encode_str(config), geoptr)
        )
        if geoip_lookup is not None:
            attached_refs[rv] = geoip_lookup
        return rv

    def normalize_event(self, event=None, raw_event=None):
        if raw_event is None:
            raw_event = _serialize_event(event)

        event = _encode_raw_event(raw_event)
        rv = self._methodcall(lib.relay_store_normalizer_normalize_event, event)
        return json.loads(decode_str(rv, free=True))


def _serialize_event(event):
    raw_event = json.dumps(event, ensure_ascii=False)
    if isinstance(raw_event, str):
        raw_event = raw_event.encode("utf-8", errors="replace")
    return raw_event


def _encode_raw_event(raw_event):
    event = encode_str(raw_event, mutable=True)
    rustcall(lib.relay_translate_legacy_python_json, event)
    return event


def is_glob_match(
    value,
    pat,
    double_star=False,
    case_insensitive=False,
    path_normalize=False,
    allow_newline=False,
):
    flags = 0
    if double_star:
        flags |= lib.GLOB_FLAGS_DOUBLE_STAR
    if case_insensitive:
        flags |= lib.GLOB_FLAGS_CASE_INSENSITIVE
        # Since on the C side we're only working with bytes we need to lowercase the pattern
        # and value here.  This works with both bytes and unicode strings.
        value = value.lower()
        pat = pat.lower()
    if path_normalize:
        flags |= lib.GLOB_FLAGS_PATH_NORMALIZE
    if allow_newline:
        flags |= lib.GLOB_FLAGS_ALLOW_NEWLINE

    if isinstance(value, str):
        value = value.encode("utf-8")
    return rustcall(lib.relay_is_glob_match, make_buf(value), encode_str(pat), flags)


def is_codeowners_path_match(value, pattern):
    if isinstance(value, str):
        value = value.encode("utf-8")
    return rustcall(
        lib.relay_is_codeowners_path_match, make_buf(value), encode_str(pattern)
    )


def validate_pii_config(config):
    """
    Validate a PII config against the schema. Used in project options UI.

    The parameter is a JSON-encoded string. We should pass the config through
    as a string such that line numbers from the error message match with what
    the user typed in.
    """
    assert isinstance(config, str)
    raw_error = rustcall(lib.relay_validate_pii_config, encode_str(config))
    error = decode_str(raw_error, free=True)
    if error:
        raise ValueError(error)


def convert_datascrubbing_config(config):
    """
    Convert an old datascrubbing config to the new PII config format.
    """
    raw_config = encode_str(json.dumps(config))
    raw_rv = rustcall(lib.relay_convert_datascrubbing_config, raw_config)
    return json.loads(decode_str(raw_rv, free=True))


def pii_strip_event(config, event):
    """
    Scrub an event using new PII stripping config.
    """
    raw_config = encode_str(json.dumps(config))
    raw_event = encode_str(json.dumps(event))
    raw_rv = rustcall(lib.relay_pii_strip_event, raw_config, raw_event)
    return json.loads(decode_str(raw_rv, free=True))


def pii_selector_suggestions_from_event(event):
    """
    Walk through the event and collect selectors that can be applied to it in a
    PII config. This function is used in the UI to provide auto-completion of
    selectors.
    """
    raw_event = encode_str(json.dumps(event))
    raw_rv = rustcall(lib.relay_pii_selector_suggestions_from_event, raw_event)
    return json.loads(decode_str(raw_rv, free=True))


def parse_release(release):
    """Parses a release string into a dictionary of its components."""
    return json.loads(
        decode_str(rustcall(lib.relay_parse_release, encode_str(release)), free=True)
    )


def compare_version(a, b):
    """Compares two versions with each other and returns 1/0/-1."""
    return rustcall(lib.relay_compare_versions, encode_str(a), encode_str(b))


def validate_sampling_condition(condition):
    """
    Validate a dynamic rule condition. Used in dynamic sampling serializer.
    The parameter is a string containing the rule condition as JSON.
    """
    assert isinstance(condition, str)
    raw_error = rustcall(lib.relay_validate_sampling_condition, encode_str(condition))
    error = decode_str(raw_error, free=True)
    if error:
        raise ValueError(error)


def validate_sampling_configuration(condition):
    """
    Validate the whole sampling configuration. Used in dynamic sampling serializer.
    The parameter is a string containing the rules configuration as JSON.
    """
    assert isinstance(condition, str)
    raw_error = rustcall(
        lib.relay_validate_sampling_configuration, encode_str(condition)
    )
    error = decode_str(raw_error, free=True)
    if error:
        raise ValueError(error)


def validate_project_config(config, strict: bool):
    """Validate the whole project config.

    :param strict: Whether or not to check for unknown fields.
    """
    assert isinstance(config, str)
    raw_error = rustcall(lib.relay_validate_project_config, encode_str(config), strict)
    error = decode_str(raw_error, free=True)
    if error:
        raise ValueError(error)


def normalize_global_config(config):
    """Normalize the global config.

    Normalization consists of deserializing and serializing back the given
    global config. If deserializing fails, throw an exception. Note that even if
    the roundtrip doesn't produce errors, the given config may differ from
    normalized one.

    :param config: the global config to validate.
    """
    serialized = json.dumps(config)
    normalized = rustcall(lib.normalize_global_config, encode_str(serialized))
    rv = decode_str(normalized, free=True)
    try:
        return json.loads(rv)
    except json.JSONDecodeError:
        raise ValueError(rv)


def run_dynamic_sampling(sampling_config, root_sampling_config, dsc, event):
    """
    Runs dynamic sampling on an event and returns the merged rules together with the sample rate.
    """
    assert isinstance(sampling_config, str)
    assert isinstance(root_sampling_config, str)
    assert isinstance(dsc, str)
    assert isinstance(event, str)

    result_json = rustcall(
        lib.run_dynamic_sampling,
        encode_str(sampling_config),
        encode_str(root_sampling_config),
        encode_str(dsc),
        encode_str(event),
    )

    return json.loads(decode_str(result_json, free=True))
