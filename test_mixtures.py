from decimal import Decimal

import mongoengine as mongo
import pytest

import field_values
from mixtures import make_fixture


@pytest.fixture(scope="module")
def mongo_document():
    class DummyEmbeddedDoc(mongo.EmbeddedDocument):
        embedded_foo = mongo.StringField(default='foo')
        embedded_created = mongo.DateTimeField()
        embedded_email = mongo.EmailField()

    class DummyModel(mongo.Document):
        foo = mongo.StringField()
        created = mongo.DateTimeField()
        email = mongo.EmailField()
        name = mongo.StringField(max_length=25)
        overridden_field = mongo.StringField()
        flag = mongo.BooleanField()
        age = mongo.IntField(min_value=5, max_value=35)
        daily_ice_cream_capacity = mongo.IntField()
        favorites = mongo.ListField(mongo.StringField(max_length=50))
        price = mongo.DecimalField(min_value=Decimal(6), max_value=Decimal(10))
        byte = mongo.BinaryField(max_bytes=85)
        embedded_things = mongo.EmbeddedDocumentField(DummyEmbeddedDoc)
        flavors = mongo.StringField(choices=['chocolate', 'vanilla', 'strawberry'])  # noqa

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
    assert mixture_data['id'] is None


def test_datetime_field_mixture(mixture_data):
    assert mixture_data['created'] == 'date'


def test_email_field_mixture(mixture_data):
    email = mixture_data['email']
    assert len(email) == 100
    assert len(email.split('@')[0]) == 88


def test_boolean_field_mixture(mixture_data):
    assert isinstance(mixture_data['flag'], bool)


def test_int_field_mixture(mixture_data):
    age = mixture_data['age']
    assert isinstance(age, int)
    assert 5 <= age <= 35


def test_decimal_field_mixture(mixture_data):
    price = mixture_data['price']
    assert isinstance(price, Decimal)
    assert Decimal(6) <= price <= Decimal(10)


def test_list_field_mixture(mixture_data):
    favorites = mixture_data['favorites']
    assert isinstance(favorites, list)
    assert favorites == []


def test_binary_field_mixture(mixture_data):
    byte = mixture_data['byte']
    assert isinstance(byte, basestring)
    assert len(byte) == 85


def test_embedded_document_field(mixture_data):
    emb_doc = mixture_data['embedded_things']
    assert len(emb_doc._fields.keys()) == 3
    assert emb_doc['embedded_foo'] == 'foo'


def test_objectid_field(mixture_data):
    document_id = mixture_data['id']
    assert document_id is None
