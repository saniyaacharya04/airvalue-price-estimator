const API_BASE = "";

function saveToken(t) {
  localStorage.setItem("token", t);
}

function getToken() {
  return localStorage.getItem("token");
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/index.html";
}

/* ---------------- AUTH ---------------- */

async function login() {
  const email = document.getElementById("login_email").value;
  const password = document.getElementById("login_password").value;

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  if (!res.ok) {
    document.getElementById("loginMsg").innerText = data.detail || "Login failed";
    return;
  }

  saveToken(data.access_token);
  window.location.href = "/dashboard.html";
}

async function signup() {
  const email = document.getElementById("signup_email").value;
  const password = document.getElementById("signup_password").value;

  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  document.getElementById("signupMsg").innerText =
    res.ok ? "Account created. Please login." : (data.detail || "Signup failed");
}

/* ---------------- FEATURE NORMALIZATION ---------------- */

/*
Backend ML model expects:
- bedrooms
- bathrooms
- location_score (1–10)
- amenities_score (1–10)
*/

function computeLocationScore(zipcode) {
  // Simple heuristic for demo purposes
  const z = Number(zipcode);
  if (z >= 10000 && z <= 19999) return 8;
  if (z >= 20000 && z <= 39999) return 6;
  return 5;
}

function computeAmenitiesScore() {
  let score = 5;
  if (document.getElementById("wifi").checked) score += 2;
  if (document.getElementById("ac").checked) score += 2;
  if (document.getElementById("entire").checked) score += 1;
  return Math.min(score, 10);
}

/* ---------------- PREDICT ---------------- */

async function predictPrice() {
  const features = {
    bedrooms: Number(document.getElementById("bedrooms").value),
    bathrooms: Number(document.getElementById("bathrooms").value),
    location_score: computeLocationScore(
      document.getElementById("zipcode").value
    ),
    amenities_score: computeAmenitiesScore()
  };

  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getToken()}`
    },
    body: JSON.stringify({ features })
  });

  const data = await res.json();

  if (!res.ok) {
    document.getElementById("predictResult").innerText =
      data.detail || "Prediction failed";
    return;
  }

  document.getElementById("predictResult").innerText =
    `Predicted Price: ₹${data.predicted_price}`;
}

/* ---------------- HISTORY ---------------- */

async function loadHistory() {
  const res = await fetch(`${API_BASE}/history`, {
    headers: { "Authorization": `Bearer ${getToken()}` }
  });

  const data = await res.json();
  const list = document.getElementById("propsList");
  list.innerHTML = "";

  data.forEach(p => {
    const li = document.createElement("li");
    li.innerText =
      `₹${p.predicted_price} — ${new Date(p.created_at).toLocaleString()}`;
    list.appendChild(li);
  });
}

/* ---------------- INIT ---------------- */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("logoutBtn")) {
    document.getElementById("logoutBtn").onclick = logout;
  }
  if (document.getElementById("loginBtn")) {
    document.getElementById("loginBtn").onclick = login;
  }
  if (document.getElementById("signupBtn")) {
    document.getElementById("signupBtn").onclick = signup;
  }
  if (document.getElementById("predictBtn")) {
    document.getElementById("predictBtn").onclick = predictPrice;
  }
});
