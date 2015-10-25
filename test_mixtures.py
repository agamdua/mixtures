import mongoengine as mongo
import pytest

import field_values
from mixtures import make_fixture


@pytest.fixture(scope="module")
def mongo_document():
    class DummyModel(mongo.Document):
        foo = mongo.StringField()
        created = mongo.DateTimeField()
        email = mongo.EmailField()
        name = mongo.StringField(max_length=25)
        overridden_field = mongo.StringField()
        flag = mongo.BooleanField()

    return DummyModel


@pytest.fixture
def mixture_data(mongo_document, monkeypatch):
    class PatchDateTime(object):
        @classmethod
        def now(cls):
            return 'date'

    monkeypatch.setattr(
        field_values,
        'datetime',
        PatchDateTime,
    )
    return make_fixture(mongo_document, overridden_field='override, woot')


def test_overridden_field(mixture_data):
    assert mixture_data['overridden_field'] == 'override, woot'


def test_string_field_mixture(mixture_data):
    # we can only assert what we know about the random data
    assert len(mixture_data['foo']) == 100
    assert len(mixture_data['name']) == 25


def test_objectid_field_mixture(mixture_data):
    assert int(mixture_data['id'])


def test_datetime_field_mixture(mixture_data):
    assert mixture_data['created'] == 'date'


def test_email_field_mixture(mixture_data):
    email = mixture_data['email']
    assert len(email) == 100
    assert len(email.split('@')[0]) == 88


def test_boolean_field_mixture(mixture_data):
    assert isinstance(mixture_data['flag'], bool)
