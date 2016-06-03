from __future__ import unicode_literals

import random
import six

from collections import namedtuple
from datetime import datetime
from decimal import Decimal
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
    def get_string_length(cls, field):
        interval = cls.get_inclusive_interval(field)
        return interval.stop - interval.start

    @classmethod
    def get_random_string(cls, string_range):
        return ''.join(
            random.choice(ascii_uppercase) for i in string_range
        )


class FieldHelperMixin(StringFieldMixin):
    # TODO: rethink inheritance hierarchy, luckily this doesn't affect the
    # user in any way
    @classmethod
    def get_value_based_inclusive_interval(cls, field, max_value=None):
        """
        This is applicable to fields with max_value and min_value as
        validators.

        Note:
            1. This is different from fields with max_length as a validator
            2. This means that the two methods based on value and length
                are almost the same method but for the max_* attribute
                that is being checked. Probably need to DRY this out at
                some point.
        """
        if field.max_value is None:
            field.max_value = max_value or MAX_LENGTH

        if field.min_value is None:
            field.min_value = 0

        Interval = namedtuple('interval', ['start', 'stop'])

        return Interval(start=field.min_value, stop=field.max_value)

    @classmethod
    def get_inclusive_interval(cls, field, max_length=None):
        if field.max_length is None:
            field.max_length = max_length or MAX_LENGTH

        if field.min_length is None:
            field.min_length = 0

        Interval = namedtuple('interval', ['start', 'stop'])

        return Interval(start=field.min_length, stop=field.max_length)

    @classmethod
    def get_range(cls, field):
        interval = cls.get_inclusive_interval(field)
        return range(interval.start, interval.stop)


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

        string_range = cls.get_range(field)

        return cls.get_random_string(string_range)

    @classmethod
    def make_objectid_field_value(cls, field):
        return six.text_type(random.randint(1, 10000))

    @classmethod
    def make_email_field_value(cls, field):
        length = cls.get_string_length(field)
        range_length = length - 12  # 12 is the length of "@example.com"

        return "{}@example.com".format(
            cls.get_random_string(range(range_length))
        )

    @classmethod
    def make_datetime_field_value(cls, field):
        return six.text_type(datetime.now())

    @classmethod
    def make_boolean_field_value(cls, field):
        return random.choice((True, False))

    @classmethod
    def make_int_field_value(cls, field):
        interval = cls.get_value_based_inclusive_interval(field)
        return random.randrange(interval.start, interval.stop)

    @classmethod
    def make_list_field_value(cls, field):
        """
        The default behavior of mongoengine is to store an empty list,
        this just mimics that.

        What it looks like is that the default is not created while
        the object is instantiated, the default is actually created
        later on in the process.

        Since this library makes no assumptions about what you want
        to do with the mongo model object this function is provided
        to "force" a default value before one ever worries about
        actually hitting mongo.

        TODO:
            Should really look into at what point the defaults are
            applied in case there's a good reason this is not done
            during creation of the object in memory.
        """
        return []

    @classmethod
    def make_decimal_field_value(cls, field):
        return Decimal(cls.make_int_field_value(field))
