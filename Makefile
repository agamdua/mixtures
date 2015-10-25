test:
	py.test --cov-report term-missing --cov=. -s .

flake8:
	flake8 .

check: flake8 test
