package: clean
	python setup.py sdist bdist_wheel

clean:
	rm -fr build dist *.egg-info

uptest: package
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

up: package
	python -m twine upload dist/*
