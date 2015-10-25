Mixtures - MongoEngine fixtures
===============================

[![Build Status](https://travis-ci.org/agamdua/mixtures.svg?branch=develop)](https://travis-ci.org/agamdua/mixtures)
[![Coverage Status](https://coveralls.io/repos/agamdua/mixtures/badge.svg?branch=develop&service=github)](https://coveralls.io/github/agamdua/mixtures?branch=develop)


Super simple fixtures, pass in a model class and mixtures will do the rest
by generating random data after introspecting the fields in the model class.

Mixtures has been inspired by [model_mommy](https://github.com/vandersonmota/model_mommy)
for django.


* Free software: BSD license

Usage
-----

```python
import mongoengine as mongo
from mixtures import make_fixture

class MongoModel(mongo.Document):
	foo = mongo.StringField(max_length=25)
	
test_data = make_fixture(MongoModel)

print(test_data)
{'foo': u'AZZQNMTKMOAQRVHGEJDUJITMD', 'id': u'1514'}
```

Upcoming
--------

* generation of test data as json or model object
	(at the moment we generate a dict)

* Overriding fields with specifc data - when you do not want random data

* stable API


Status
------

Not even alpha, if we are being completely honest
