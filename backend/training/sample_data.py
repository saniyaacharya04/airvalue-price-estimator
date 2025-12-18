"""
NOTE:
This file is used for offline data preparation.
It is not executed in production.
"""

# This writes a small sample CSV to dataset/sample_properties.csv (for reference)
from .ml_model import generate_synthetic_dataset
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "dataset", "sample_properties.csv")
OUT = os.path.abspath(OUT)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
generate_synthetic_dataset(csv_out_path=OUT, n=200)
