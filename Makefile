# ================================
# AirValue — Makefile
# ================================

PYTHON=python
PIP=pip
BACKEND_DIR=backend
APP_MODULE=app.main:app
ENV_FILE=.env

# -------------------------------
# Setup & Dependencies
# -------------------------------

install:
	$(PIP) install -r $(BACKEND_DIR)/requirements.txt

# -------------------------------
# Development
# -------------------------------

run:
	cd $(BACKEND_DIR) && uvicorn $(APP_MODULE) --reload

run-prod:
	cd $(BACKEND_DIR) && uvicorn $(APP_MODULE) --host 0.0.0.0 --port 8000

# -------------------------------
# ML Training
# -------------------------------

train:
	cd $(BACKEND_DIR)/training && $(PYTHON) train_model.py

# -------------------------------
# Testing
# -------------------------------

e2e:
	bash $(BACKEND_DIR)/scripts/e2e_test.sh

# -------------------------------
# Cleanup
# -------------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# -------------------------------
# Help
# -------------------------------

help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make run         Run backend (dev mode)"
	@echo "  make run-prod    Run backend (prod mode)"
	@echo "  make train       Train ML model"
	@echo "  make e2e         Run end-to-end tests"
	@echo "  make clean       Cleanup cache files"
