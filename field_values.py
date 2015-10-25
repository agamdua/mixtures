from __future__ import unicode_literals

import random

from collections import namedtuple
from datetime import datetime
from string import ascii_uppercase

MAX_LENGTH = 100  # just for simplicity


def get_factory_func(field):
    return getattr(
        FieldValue, "make_{}_field_value".format(
            field.__class__.__name__.split('Field')[0].lower()
        )
    )


def get_random_value(field):
    """
    Calls the dispatch method (``get_factory_func``) and passes the field
    obj argument to the callable returned.

    Returns:
        random value depending on field type and constraints in the field
            object
    """
    func = get_factory_func(field)
    return func(field)


class StringFieldMixin(object):
    @classmethod
    def get_string_inclusive_interval(cls, field, max_length=None):
        if field.max_length is None:
            field.max_length = max_length or MAX_LENGTH

        if field.min_length is None:
            field.min_length = 0

        StringInterval = namedtuple('string_interval', ['start', 'end'])

        return StringInterval(start=field.min_length, end=field.max_length)

    @classmethod
    def get_string_range(cls, field):
        interval = cls.get_string_inclusive_interval(field)
        return range(interval.start, interval.end)

    @classmethod
    def get_string_length(cls, field):
        interval = cls.get_string_inclusive_interval(field)
        return interval.end - interval.start

    @classmethod
    def get_random_string(cls, string_range):
        return ''.join(
            random.choice(ascii_uppercase) for i in string_range
        )


class FieldHelperMixin(StringFieldMixin):
    pass


class FieldValue(FieldHelperMixin):
    @classmethod
    def make_string_field_value(cls, field):
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

        string_range = cls.get_string_range(field)

        return cls.get_random_string(string_range)

    @classmethod
    def make_objectid_field_value(cls, field):
        return unicode(random.randint(1, 10000))

    @classmethod
    def make_email_field_value(cls, field):
        length = cls.get_string_length(field)
        range_length = length - 12  # 12 is the length of "@example.com"

        return "{}@example.com".format(
            cls.get_random_string(range(range_length))
        )

    @classmethod
    def make_datetime_field_value(cls, field):
        return unicode(datetime.now())
