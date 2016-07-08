Mixtures - MongoEngine fixtures
===============================

[![Build Status](https://travis-ci.org/agamdua/mixtures.svg?branch=develop)](https://travis-ci.org/agamdua/mixtures)
[![Coverage Status](https://coveralls.io/repos/agamdua/mixtures/badge.svg?branch=develop&service=github)](https://coveralls.io/github/agamdua/mixtures?branch=develop)


Super simple fixtures, pass in a model class and mixtures will do the rest
by generating random data after introspecting the fields in the model class.

Mixtures has been inspired by [model_mommy](https://github.com/vandersonmota/model_mommy).


* Free software: BSD license

Usage
-----

```python
import mongoengine as mongo
from mixtures import make_fixture

class MongoModel(mongo.Document):
    flag = mongo.BooleanField()
    created = mongo.DateTimeField()
    email = mongo.EmailField()
    foo = mongo.StringField()
    name = mongo.StringField(max_length=25)
    overridden_field = mongo.StringField()
	
test_data = make_fixture(MongoModel, overridden_field='custom data')
```

```python
>>> from pprint import pprint
>>> pprint(test_data)
<MongoModel: MongoModel object>

>>> pprint(test_data.__dict__)
{'_data': {'created': datetime.datetime(2016, 7, 8, 20, 2, 46, 519796),
           'email': u'WDNGPGOBYDOVTIGHXRFGRQJMUXGTOBMJQFRSLBQMNIHPWZJTKLPYHVCNMJMJWDRETXEHSVZBMMCVHMTMMYJRGWUN@example.com',
           'flag': True,
           'foo': u'LRIHPGMMVGPZBAJOWQKIGXLGDRZFEQCBMRRAWMNZWJQAOIUZPWPSBHXRWQEIWWUFXLJPLQJRRUIGIJJGZPFQWHJJRFEOSJEAHDMP',
           'id': None,
           'name': u'HQEPPMXRUCRNGRGORCICJOPKQ',
           'overridden_field': u'custom data'},
 '_initialised': True}
```

Status
------

Releasing alpha now
