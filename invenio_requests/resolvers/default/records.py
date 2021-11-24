# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resolver for records."""

from ..base import EntityProxy, EntityResolver


class RecordProxy(EntityProxy):
    """Resolver proxy for a Record entity."""

    def __init__(self, ref_dict, record_cls):
        """Constructor.

        :param record_cls: The record class to use.
        """
        super().__init__(ref_dict)
        self.record_cls = record_cls

    def _resolve(self):
        """Resolve the Record from the proxy's reference dict."""
        pid_value = self._parse_ref_dict_id(self._ref_dict)
        return self.record_cls.pid.resolve(pid_value)

    def get_need(self):
        """Return None since Needs are not applicable to records."""
        return None


class RecordResolver(EntityResolver):
    """Resolver for records."""

    def __init__(self, record_cls, type_key="record", proxy_cls=RecordProxy):
        """Constructor.

        :param record_cls: The record class to use.
        :param type_key: The value to use for the TYPE part of the reference dicts.
        """
        self.record_cls = record_cls
        self.type_key = type_key
        self.proxy_cls = proxy_cls

    def matches_entity(self, entity):
        """Check if the entity is a record."""
        return isinstance(entity, self.record_cls)

    def _reference_entity(self, entity):
        """Create a reference dict for the given record."""
        return {self.type_key: str(entity.pid.pid_value)}

    def matches_reference_dict(self, ref_dict):
        """Check if the reference dict references a request."""
        return self._parse_ref_dict_type(ref_dict) == self.type_key

    def _get_entity_proxy(self, ref_dict):
        """Return a RecordProxy for the given reference dict."""
        return self.proxy_cls(ref_dict, self.record_cls)