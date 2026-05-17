PYTHON=uv run --with pybtex --with jinja2 python
BIBGEN=bib/generate-pubs.py

# targets that aren't filenames
.PHONY: all clean deploy

all: _includes/pubs.html _data/pubs.yml _site/index.html

BUILDARGS :=
_site/index.html:
	bundle exec jekyll build $(BUILDARGS)

_includes/pubs.html: bib/pubs.bib bib/publications.tmpl
	mkdir -p _includes
	$(PYTHON) $(BIBGEN) $+ > $@

_data/pubs.yml: bib/pubs.bib bib/pubs-yml.tmpl
	mkdir -p _includes
	$(PYTHON) $(BIBGEN) $+ > $@

_site/index.html: $(wildcard *.html) _includes/pubs.html _config.yml \
	_layouts/default.html

clean:
	$(RM) -r _site _includes/pubs.html

HOST := yourwebpage.com
PATHSVR := www/
deploy: clean all
	rsync --compress --recursive --checksum --itemize-changes --delete -e ssh _site/ $(HOST):$(PATHSVR)
