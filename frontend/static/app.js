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

/* ---------------- PREDICT ---------------- */

async function predictPrice(save = false) {
  const features = {
    bedrooms: Number(document.getElementById("bedrooms").value),
    bathrooms: Number(document.getElementById("bathrooms").value),
    area: Number(document.getElementById("area").value),
    zipcode_feat: Number(document.getElementById("zipcode").value),
    has_wifi: document.getElementById("wifi").checked ? 1 : 0,
    has_ac: document.getElementById("ac").checked ? 1 : 0,
    is_entire_place: document.getElementById("entire").checked ? 1 : 0
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
    li.innerText = `₹${p.predicted_price} — ${new Date(p.created_at).toLocaleString()}`;
    list.appendChild(li);
  });
}

/* ---------------- DASHBOARD ---------------- */

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
    document.getElementById("predictBtn").onclick = () => predictPrice(false);
  }
  if (document.getElementById("saveBtn")) {
    document.getElementById("saveBtn").onclick = () => predictPrice(true);
  }
});
