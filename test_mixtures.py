import mongoengine as mongo
import pytest

from mixtures import make_fixture

@pytest.fixture
def mongo_document():
    class DummyModel(mongo.Document):
        foo = mongo.StringField()
        created = mongo.DateTimeField()

    return DummyModel

def test_make_fixture(mongo_document):
    test_data = make_fixture(mongo_document)

    # we can only assert what we know about the random data
    assert len(test_data['foo']) == 100
    assert int(test_data['id'])
    assert test_data['created'] is None
