#!/usr/bin/env bash

set -e

API="http://127.0.0.1:8000"

echo "======================================"
echo "AirValue E2E Validation Started"
echo "======================================"

EMAIL="test_$(date +%s)@airvalue.dev"
PASSWORD="StrongPass123"

echo ""
echo "1️⃣ Health Check"
curl -fs "$API/docs" > /dev/null
echo "✔ API is reachable"

echo ""
echo "2️⃣ User Registration"
REGISTER_RESPONSE=$(curl -sS --fail \
  -X POST "$API/auth/register" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

echo "$REGISTER_RESPONSE" | grep -q "\"email\"" || {
  echo "❌ Registration failed:"
  echo "$REGISTER_RESPONSE"
  exit 1
}
echo "✔ User registered: $EMAIL"

echo ""
echo "3️⃣ User Login"
LOGIN_RESPONSE=$(curl -sS --fail \
  -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

TOKEN=$(python - << PY
import json
resp = """$LOGIN_RESPONSE""".strip()
if not resp:
    raise SystemExit("Empty login response")
data = json.loads(resp)
print(data.get("access_token", ""))
PY
)

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to extract JWT token"
  echo "Raw login response:"
  echo "$LOGIN_RESPONSE"
  exit 1
fi

echo "✔ JWT token received"

echo ""
echo "4️⃣ Price Prediction"
PREDICT_RESPONSE=$(curl -sS --fail \
  -X POST "$API/predict" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "features": {
      "bedrooms": 2,
      "bathrooms": 1,
      "location_score": 7,
      "amenities_score": 8
    }
  }')

PRICE=$(python - << PY
import json
print(json.loads("""$PREDICT_RESPONSE""")["predicted_price"])
PY
)

echo "✔ Prediction successful: ₹$PRICE"

echo ""
echo "5️⃣ Prediction History"
HISTORY_RESPONSE=$(curl -sS --fail \
  "$API/history" \
  -H "Authorization: Bearer $TOKEN")

COUNT=$(python - << PY
import json
print(len(json.loads("""$HISTORY_RESPONSE""")))
PY
)

echo "✔ History entries found: $COUNT"

echo ""
echo "6️⃣ Premium Endpoint Lock Check"
PREMIUM_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "$API/premium/bulk-predict" \
  -H "Authorization: Bearer $TOKEN")

if [ "$PREMIUM_STATUS" != "402" ]; then
  echo "❌ Premium endpoint is not locked correctly (status=$PREMIUM_STATUS)"
  exit 1
fi

echo "✔ Premium feature correctly locked (402)"

echo ""
echo "======================================"
echo "🎉 ALL E2E TESTS PASSED SUCCESSFULLY"
echo "======================================"
