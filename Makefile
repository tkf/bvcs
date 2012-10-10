all: README bvcs/__init__.py

clean:
	rm -f README

README: generate_readme.py README-header.rst
	python generate_readme.py > README

bvcs/__init__.py: README-header.rst
	cd bvcs && cog.py -r __init__.py

upload:
	python setup.py register sdist upload
