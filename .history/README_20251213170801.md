# AirValue — Airbnb Price Estimator

AirValue is an end-to-end, production-style Airbnb price prediction system that estimates nightly rental prices based on property features and location signals.

This project demonstrates full-stack ownership — from machine learning model training to secure backend APIs and a working frontend — and is designed for resume shortlisting, GitHub review, and technical interviews.

---

## One-Line Value Proposition

Predict fair Airbnb prices using machine learning, with user authentication, history tracking, and premium feature placeholders, all running locally.

---

## Target Users

* Property hosts wanting to estimate competitive pricing
* Data science and machine learning recruiters evaluating applied ML skills
* Backend and software engineering interviewers assessing API and system design
* Students looking for a real-world ML and backend project reference

---

## Problem Statement

Setting the right Airbnb price is difficult due to multiple interacting factors such as amenities, size, and location, as well as market variability and lack of transparent pricing tools.

AirValue addresses this by training a regression model on structured property features and exposing predictions through a secure, user-facing system.

---

## System Overview

Frontend (HTML/CSS/JavaScript)
↓
FastAPI Backend (Authentication, APIs)
↓
ML Inference Service (RandomForest Regressor)
↓
SQLite Database (Users and Predictions)

---

## Key Features

### Free Features (Fully Implemented)

* User registration and login with JWT-based authentication
* Single-property price prediction using a trained ML model
* Real-time ML inference through backend API
* Prediction history stored per user
* Clean, accessible frontend UI
* Input validation and structured error handling

### Premium Features (Placeholder Only)

* Bulk CSV batch predictions
* Advanced analytics dashboard
* Upgraded ML model (for example, XGBoost)
* Premium upgrade flow

All premium features are clearly marked and intentionally locked with placeholder responses.

---

## Technology Stack and Justification

Backend: FastAPI for fast, modern, production-ready APIs
Machine Learning: scikit-learn RandomForest for robust tabular regression
Authentication: JWT using python-jose for stateless security
Database: SQLite with SQLAlchemy ORM for portability and clean modeling
Frontend: HTML, CSS, and Vanilla JavaScript for simplicity and clarity
Model Persistence: joblib for saving and loading trained models

All tools are free, industry-standard, and fully runnable on a local machine.

---

## Project Structure

```
airvalue/
├── backend/
│   ├── app/
│   │   ├── api/          # Auth, predict, history, premium routes
│   │   ├── core/         # Security and auth dependencies
│   │   ├── db/           # Database engine and session
│   │   ├── ml/           # Model training and inference
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI application entry point
│   ├── airvalue.db
│   ├── airvalue_rf_model.joblib
│   └── requirements.txt
├── frontend/
│   └── static/           # HTML, CSS, and JS frontend
├── dataset/
│   └── sample_properties.csv
├── README.md
└── LICENSE
```

---

## Authentication and Security

* Password hashing using bcrypt
* JWT access tokens with expiration
* Role-based access control (free and premium users)
* Explicit enforcement of premium feature restrictions
* No hard-coded secrets

---

## Machine Learning Model Details

Algorithm: RandomForestRegressor

Input Features:

* Bedrooms
* Bathrooms
* Area (square feet)
* Encoded zipcode
* WiFi availability
* Air conditioning availability
* Entire property flag

Output:

* Predicted nightly rental price

The model is trained offline and loaded at runtime for inference.

---

## Local Setup and Run Instructions

Create and activate environment:

```bash
conda create -n airvalue-py310 python=3.10
conda activate airvalue-py310
```

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Run backend server:

```bash
uvicorn app.main:app --reload
```

Open application:

```
http://127.0.0.1:8000
```

---

## Sample API Usage

Predict price (authenticated request):

```http
POST /predict
Authorization: Bearer <JWT>
Content-Type: application/json
```

```json
{
  "features": {
    "bedrooms": 2,
    "bathrooms": 1,
    "area": 850,
    "zipcode_feat": 12,
    "has_wifi": 1,
    "has_ac": 1,
    "is_entire_place": 1
  }
}
```

---

## Failure Modes and Edge Cases

* Invalid credentials return authentication errors
* Missing or malformed input features trigger validation failures
* Unauthorized access is blocked by JWT enforcement
* Premium-only endpoints return locked responses for free users
* Empty prediction history is handled gracefully
* Model loading errors fail safely with clear logs

---

## Resume-Ready Highlights

* Designed and implemented an end-to-end ML-powered pricing system using FastAPI and scikit-learn
* Built secure JWT-based authentication with role-based access control
* Deployed a trained regression model for real-time inference
* Implemented persistent storage for user predictions using SQLAlchemy
* Integrated frontend UI with backend APIs for a complete user workflow

---

## Interview Discussion Topics

* Model selection for tabular data
* Feature engineering decisions
* JWT-based authentication design
* API design and validation
* Free versus premium feature gating
* Scaling considerations and trade-offs

---

## Future Enhancements

* Migration from SQLite to PostgreSQL
* Background model retraining pipelines
* Geospatial feature enrichment
* Payment integration for premium access
* Model explainability and analytics

---

## License

This project is released under the MIT License.

---

## Final Note

This project was intentionally scoped to be end-to-end, executable, and interview-defendable within a realistic timeframe for a single engineer. It reflects real-world system design and applied machine learning practices rather than a tutorial-style demo.

---
