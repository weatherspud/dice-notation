python_version := 3.5

.PHONY: check
check: pylint mypy pep8 test

.PHONY: test
test: ve
	. ve/bin/activate && find test/unit -name test*.py | PYTHONPATH=. xargs -n 1 python

ve:
	virtualenv $@ --python=python$(python_version)
	. ./$@/bin/activate && pip install -r requirements.txt

repl:
	. ve/bin/activate && python

lintable := dice test

.PHONY:
pylint: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs pylint --rcfile ./.pylintrc -d missing-docstring

.PHONY: pep8
pep8: ve
	. ve/bin/activate && find $(lintable) -name *.py | xargs pep8 --max-line-length=100

.PHONY: mypy
mypy: ve
	. ve/bin/activate && find $(lintable) -name *.py \
	  | xargs -n 1 mypy --silent-imports --strict-optional --disallow-untyped-defs
