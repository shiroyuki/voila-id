PYI=python
SERVICE_FLAG=
STATIC_SOURCE_PATH=docs/source
STATIC_DOCTREE_PATH=docs/build/doctrees
STATIC_HTML_PATH=docs/build/html
SCSS_PATH=static/scss
CSS_PATH=static/css

default:
	@echo 'Static command for NEP Core'
	@echo '  make service:  active the service'
	@echo '  make css:      compile CSS from SCSS'
	@echo '  make css_live: compile CSS from SCSS and update when a file is updated'
	@echo
	@echo 'For more options, run "./console".'

service: css
	@$(PYI) server.py $(SERVICE_FLAG)

web:
	sphinx-build -b html -d $(STATIC_DOCTREE_PATH) $(STATIC_SOURCE_PATH) $(STATIC_HTML_PATH)

css:
	@sass --update $(SCSS_PATH):$(CSS_PATH) --style compressed

css_live:
	@sass --watch $(SCSS_PATH):$(CSS_PATH) --style compressed
