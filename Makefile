.PHONY: env install train run clean

# --------------------------------------------------
# Environment
# --------------------------------------------------

env:
	@echo "Activate conda environment first:"
	@echo "conda activate airvalue-py310"

# --------------------------------------------------
# Install dependencies
# --------------------------------------------------

install:
	pip install -r backend/requirements.txt

# --------------------------------------------------
# Train ML model (offline)
# --------------------------------------------------

train:
	python backend/app/ml/train.py

# --------------------------------------------------
# Run backend server
# --------------------------------------------------

run:
	cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# --------------------------------------------------
# Cleanup artifacts
# --------------------------------------------------

clean:
	rm -f backend/airvalue_rf_model.joblib
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
