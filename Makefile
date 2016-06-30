test:
	py.test --cov-report term-missing --cov=. -s .

flake8:
	flake8 .

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -delete

ready: clean flake8 test
