# blynclight Makefile
#
VERSION=0.4.4
PYTHON= python3
SETUP_PY= setup.py
TWINE= twine
PYPI= testpypi
TEMP= build dist

.PHONY: VERSION black test sdist readme release upload

BLACK= black

all:
	@echo "VERSION=$(VERSION)"
	@echo "Targets:"
	@echo " black   - run black code formatter"
	@echo "	test    - run pytest"
	@echo "	bdist   - binary distribution"
	@echo "	sdist   - source distribution"
	@echo "	readme  - README rst checking"
	@echo "	release - VERSION=$(VERSION) readme bdist sdist"
	@echo "	upload  - release and upload to PYPI=$(PYPI)"
	@echo "	clean   - cleanup temporary files: TEMP=$(TEMP)"

VERSION:
	@echo $(VERSION) > $@

black:
	$(BLACK) -l 79 src tests contrib

test: VERSION
	$(PYTHON) $(SETUP_PY) test

bdist: VERSION
	$(PYTHON) $(SETUP_PY) bdist_wheel

sdist: VERSION
	$(PYTHON) $(SETUP_PY) sdist

readme: VERSION README.rst
	$(PYTHON) $(SETUP_PY) check -r -s

release: clean VERSION readme bdist sdist


upload: release 
	$(TWINE) upload --repository ${PYPI} dist/*

clean:
	-@$(PYTHON) $(SETUP_PY) clean >& /dev/null
	@$(RM) -rf $(TEMP) *~ *.egg-info

