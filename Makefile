PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: setup diagrams serve

setup:
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

diagrams:
	$(PYTHON) generate_diagrams.py

serve:
	@echo "Docs site: http://localhost:8000"
	$(PYTHON) -m http.server 8000
