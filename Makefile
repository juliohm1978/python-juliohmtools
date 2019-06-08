package: clean
	python setup.py sdist bdist_wheel

clean:
	rm -fr build dist *.egg-info

# uptest: package
# 	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

install: package
	python -m twine upload --u juliohm -p $(shell pass pypi-juliohm)  dist/*

localtest:
	pip install -e .

## install CRDs for testing
installg:
	kubectl apply -f test/guitars.yaml

## remove CRDs from testing
deleteg:
	kubectl delete -f test/guitars.yaml
