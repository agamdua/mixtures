import os
from setuptools import setup, find_packages

here = os.path.dirname(__file__)

__version__ = "0.0.rc1"
__author__ = "Agam Dua"

def read(filename):
    with open(os.path.join(here, filename)) as f:
        return f.read().decode("utf-8")


install_requires = read("requirements.txt").splitlines() + ["setuptools"]
tests_require = (
    read("requirements.txt").splitlines() + read("requirements-tests.txt").splitlines()[1:]
)

setup(
    name="mixtures",
    version=__version__,
    author=__author__,
    description="Fixtures library for mongoengine",
    url="https://github.com/agamdua/mixtures",
    packages=find_packages(exclude=["requirements", "tests"]),
    install_requires=install_requires,
    test_suite="tests",
    tests_require=tests_require,
    license="BSD",
    keywords="mongo mongoengine",
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

)
