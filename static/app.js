// ======================================================
// Weather Dashboard - Clean Refactored Version (SOLID)
// ======================================================

console.log("App JS loaded.");

// ------------------------------------------------------
// 1. CONSTANTS & HELPERS
// ------------------------------------------------------

const DEFAULT_CITY = "Madrid";
const DEFAULT_NAME = "Friend";

const iconUrl = code => `https://openweathermap.org/img/wn/${code}@2x.png`;

const WMO_ICON_MAP = {
  0: "01d",
  1: "02d", 2: "02d",
  3: "04d",
  45: "50d", 48: "50d",
  51: "09d", 53: "09d", 55: "09d",
  61: "10d", 63: "10d", 65: "10d",
  66: "13d", 67: "13d",
  71: "13d", 73: "13d", 75: "13d", 77: "13d",
  80: "09d", 81: "09d", 82: "09d",
  95: "11d", 96: "11d", 99: "11d"
};

const WMO_DESC_MAP = {
  0: "Clear Sky",
  1: "Mainly Clear",
  2: "Partly Cloudy",
  3: "Overcast",
  45: "Fog",
  48: "Depositing Rime Fog",
  51: "Light Drizzle",
  53: "Moderate Drizzle",
  55: "Dense Drizzle",
  61: "Slight Rain",
  63: "Moderate Rain",
  65: "Heavy Rain",
  66: "Freezing Rain (Light)",
  67: "Freezing Rain (Heavy)",
  71: "Slight Snow",
  73: "Moderate Snow",
  75: "Heavy Snow",
  77: "Snow Grains",
  80: "Rain Showers (Slight)",
  81: "Rain Showers (Moderate)",
  82: "Rain Showers (Violent)",
  95: "Thunderstorm",
  96: "Thunderstorm (Slight Hail)",
  99: "Thunderstorm (Heavy Hail)"
};

// Utility functions
const iconFromWmo = code => WMO_ICON_MAP[code] || "02d";
const descFromWmo = code => WMO_DESC_MAP[code] || "Weather";


// ------------------------------------------------------
// 2. WEATHER API MODULE
// ------------------------------------------------------

async function geocode(city) {
  const url = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("Geocoding failed");

  const data = await res.json();
  if (!data.results?.length) throw new Error(`City '${city}' not found`);

  const place = data.results[0];
  return {
    name: place.name,
    lat: place.latitude,
    lon: place.longitude
  };
}

async function forecast(lat, lon) {
  const url = new URL("https://api.open-meteo.com/v1/forecast");
  const params = {
    latitude: lat,
    longitude: lon,
    timezone: "auto",
    current: "temperature_2m,weather_code",
    daily: "weather_code,temperature_2m_max,temperature_2m_min"
  };

  Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));

  const res = await fetch(url);
  if (!res.ok) throw new Error("Forecast failed");

  return res.json();
}


// ------------------------------------------------------
// 3. RENDERING MODULE
// ------------------------------------------------------

function renderCurrent(city, current) {
  const code = Number(current.weather_code || 0);

  document.getElementById("city-name").textContent = city;
  document.getElementById("current-desc").textContent = descFromWmo(code);
  document.getElementById("temp").textContent = `${Math.round(current.temperature_2m)}°C`;

  const img = document.getElementById("icon");
  img.src = iconUrl(iconFromWmo(code));
  img.alt = descFromWmo(code);
}

function renderWeek(daily) {
  const week = document.getElementById("week");
  week.innerHTML = "";

  (daily.time || []).slice(0, 7).forEach((timestamp, i) => {
    const code = Number(daily.weather_code[i]);
    const dayCard = document.createElement("div");
    dayCard.className = "day";

    dayCard.innerHTML = `
      <div class="name">${new Date(timestamp).toLocaleDateString(undefined, { weekday: "short" })}</div>
      <img src="${iconUrl(iconFromWmo(code))}" alt="${descFromWmo(code)}">
      <div class="hi">${Math.round(daily.temperature_2m_max[i])}°</div>
      <div class="lo">${Math.round(daily.temperature_2m_min[i])}°</div>
    `;

    week.appendChild(dayCard);
  });
}

async function render(city) {
  try {
    const loc = await geocode(city);
    const data = await forecast(loc.lat, loc.lon);

    renderCurrent(loc.name, data.current);
    renderWeek(data.daily);
  } catch (err) {
    alert(err.message || "Failed to load weather");
  }
}


// ------------------------------------------------------
// 4. BACKEND PERSISTENCE HELPERS
// ------------------------------------------------------

async function loadLastCity() {
  try {
    const res = await fetch("/api/last-city");
    const json = await res.json();
    return json.last_city || DEFAULT_CITY;
  } catch {
    return DEFAULT_CITY;
  }
}

async function saveLastCity(city) {
  try {
    await fetch("/api/last-city", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ last_city: city })
    });
  } catch (err) {
    console.warn("Failed to save last city:", err);
  }
}


// ------------------------------------------------------
// 5. GREETING / NAME MODULE
// ------------------------------------------------------

function toggleNameControls(show) {
  const nameControls = document.getElementById("name-controls");
  if (nameControls) nameControls.style.display = show ? "flex" : "none";
}

function setGreeting() {
  const user = localStorage.getItem("user_name") ||
               document.getElementById("name-input")?.value ||
               DEFAULT_NAME;

  const hour = new Date().getHours();
  const greeting = hour < 12
    ? "Good Morning"
    : hour < 18
    ? "Good Afternoon"
    : "Good Evening";

  document.getElementById("greeting").textContent = `${greeting}, ${user}!`;

  toggleNameControls(!localStorage.getItem("user_name"));
}


// Save name button
document.getElementById("save-name").addEventListener("click", () => {
  const input = document.getElementById("name-input").value.trim();
  if (input) {
    localStorage.setItem("user_name", input);
    setGreeting();
  }
});

// Click greeting → update name
document.getElementById("greeting").addEventListener("click", () => {
  const saved = localStorage.getItem("user_name") || DEFAULT_NAME;
  const newName = prompt("Update your name:", saved);

  if (newName && newName.trim()) {
    localStorage.setItem("user_name", newName.trim());
    setGreeting();
  }
});


// ------------------------------------------------------
// 6. SEARCH HANDLERS
// ------------------------------------------------------

document.getElementById("go-btn").addEventListener("click", async () => {
  const city = document.getElementById("city-input").value.trim() || DEFAULT_CITY;
  await render(city);
  saveLastCity(city);
});

document.getElementById("city-input").addEventListener("keydown", e => {
  if (e.key === "Enter") document.getElementById("go-btn").click();
});


// ------------------------------------------------------
// 7. APP BOOTSTRAP
// ------------------------------------------------------

(async function bootstrap() {
  setGreeting();

  const city = await loadLastCity();
  document.getElementById("city-input").value = city;

  await render(city);
})();
