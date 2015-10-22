from __future__ import unicode_literals

import random

from string import ascii_uppercase

MAX_LENGTH = 100  # just for simplicity


def get_factory_func(field):
    return getattr(
        FieldValue, "make_{}_field_value".format(
            field.__class__.__name__.split('Field')[0].lower()
        )
    )


class FieldValue(object):
    @staticmethod
    def make_string_field_value(field):
        """
        String Field has three constraints (apart from anything
        in the super class)

        Args:
            field (StringField): actual string field object from a
            model declaration

        Returns:
            random string value
        """
        if field.regex is not None:
            raise NotImplementedError

        if field.max_length is None:
            field.max_length = MAX_LENGTH

        if field.min_length is None:
            field.min_length = 0

        string_range = range(field.min_length, field.max_length)

        return ''.join(
            random.choice(ascii_uppercase) for i in string_range
        )

    @staticmethod
    def make_objectid_field_value(field):
        return unicode(random.randint(1, 10000))
