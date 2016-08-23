from __future__ import unicode_literals

"""
MongoEngine fixtures
"""
import mongoengine as mongo

from field_values import get_random_value


def make_fixture(model_class, **kwargs):
    """
    Take the model_klass and generate a fixure for it

    Args:
        model_class (MongoEngine Document): model for which a fixture
            is needed
        kwargs (dict): any overrides instead of random values

    Returns:
        dict for now, other fixture types are not implemented yet
    """
    all_fields = get_fields(model_class)

    fields_for_random_generation = map(
        lambda x: getattr(model_class, x), all_fields
    )

    overrides = {}

    for kwarg, value in kwargs.items():
        if kwarg in all_fields:
            kwarg_field = getattr(model_class, kwarg)
            fields_for_random_generation.remove(kwarg_field)
            overrides.update({kwarg_field: value})

    random_values = get_random_values(fields_for_random_generation)

    values = dict(overrides, **random_values)

    assert len(all_fields) == len(values), (
        "Mismatch in values, {} != {}".format(
            len(all_fields), len(values)
        )
    )
    data = {k.name: v for k, v in values.items()}
    return model_class(**data)


def get_fields(model_class):
    """
    Pass in a mongo model class and extract all the attributes which
    are mongoengine fields

    Returns:
        list of strings of field attributes
    """
    return [
        attr for attr, value in model_class.__dict__.items()
        if issubclass(type(value), (mongo.base.BaseField, mongo.EmbeddedDocumentField))  # noqa
    ]


def get_random_values(fields):
    """
    Pass in a list of fields (as strings) to get a dict with the
    field name as a key and a randomly generated value as another
    """
    values = {}

    for field in fields:
        try:
            value = get_random_value(field)
        except AttributeError:
            # this can only really occur if the field is not implemented yet.
            # Silencing the exception during the prototype phase
            value = None

        values.update({field: value})

    return values
