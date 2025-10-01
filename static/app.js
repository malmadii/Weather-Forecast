console.log("App JS loaded.");

const iconUrl = code => `https://openweathermap.org/img/wn/${code}@2x.png`;
const iconFromWmo = code => {
  if ([0].includes(code)) return "01d";
  if ([1,2].includes(code)) return "02d";
  if ([3].includes(code)) return "04d";
  if ([45,48].includes(code)) return "50d";
  if ([51,53,55].includes(code)) return "09d";
  if ([61,63,65].includes(code)) return "10d";
  if ([66,67].includes(code)) return "13d";
  if ([71,73,75,77].includes(code)) return "13d";
  if ([80,81,82].includes(code)) return "09d";
  if ([95,96,99].includes(code)) return "11d";
  return "02d";
};
const descFromWmo = code => ({
  0:"Clear Sky",1:"Mainly Clear",2:"Partly Cloudy",3:"Overcast",
  45:"Fog",48:"Depositing Rime Fog",
  51:"Light Drizzle",53:"Moderate Drizzle",55:"Dense Drizzle",
  61:"Slight Rain",63:"Moderate Rain",65:"Heavy Rain",
  66:"Freezing Rain (Light)",67:"Freezing Rain (Heavy)",
  71:"Slight Snow",73:"Moderate Snow",75:"Heavy Snow",77:"Snow Grains",
  80:"Rain Showers (Slight)",81:"Rain Showers (Moderate)",82:"Rain Showers (Violent)",
  95:"Thunderstorm",96:"Thunderstorm (Slight Hail)",99:"Thunderstorm (Heavy Hail)"
}[code] || "Weather");

// --- API calls (no key needed) ---
async function geocode(city){
  const r = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1`);
  if(!r.ok) throw new Error("Geocoding failed");
  const j = await r.json();
  if(!j.results || !j.results.length) throw new Error(`City '${city}' not found`);
  const p = j.results[0];
  return { name: p.name, lat: p.latitude, lon: p.longitude };
}

async function forecast(lat, lon){
  const url = new URL("https://api.open-meteo.com/v1/forecast");
  Object.entries({
    latitude: lat, longitude: lon, timezone: "auto",
    current: "temperature_2m,weather_code",
    daily: "weather_code,temperature_2m_max,temperature_2m_min"
  }).forEach(([k,v])=>url.searchParams.set(k,v));
  const r = await fetch(url);
  if(!r.ok) throw new Error("Forecast failed");
  return r.json();
}

// --- Render functions ---
function renderCurrent(city, cur){
  document.getElementById("city-name").textContent = city;
  const code = Number(cur.weather_code || 0);
  document.getElementById("current-desc").textContent = descFromWmo(code);
  document.getElementById("temp").textContent = Math.round(cur.temperature_2m) + "°C";
  const img = document.getElementById("icon");
  img.src = iconUrl(iconFromWmo(code));
  img.alt = "icon";
}

function renderWeek(daily){
  const week = document.getElementById("week");
  week.innerHTML = "";
  const times = (daily.time || []).slice(0,7);
  times.forEach((ts,i)=>{
    const code = Number(daily.weather_code[i]);
    const card = document.createElement("div");
    card.className = "day";
    card.innerHTML = `
      <div class="name">${new Date(ts).toLocaleDateString(undefined,{weekday:'short'})}</div>
      <img src="${iconUrl(iconFromWmo(code))}" alt="">
      <div class="hi">${Math.round(daily.temperature_2m_max[i])}°</div>
      <div class="lo">${Math.round(daily.temperature_2m_min[i])}°</div>
    `;
    week.appendChild(card);
  });
}

async function render(city){
  try{
    const place = await geocode(city);
    const wx = await forecast(place.lat, place.lon);
    renderCurrent(place.name, wx.current);
    renderWeek(wx.daily);
  }catch(e){
    alert(e.message || "Failed to load weather");
  }
}

// --- Greeting (personalized, saved locally) ---
function setGreeting(){
  const saved = localStorage.getItem("user_name") || document.getElementById("name-input").value || "Friend";
  const h = new Date().getHours();
  const part = h<12 ? "Good Morning" : h<18 ? "Good Afternoon" : "Good Evening";
  document.getElementById("greeting").textContent = `${part}, ${saved}!`;
}
document.getElementById("save-name").addEventListener("click", ()=>{
  const v = document.getElementById("name-input").value.trim();
  if(v){ localStorage.setItem("user_name", v); setGreeting(); }
});

// --- Search handlers ---
document.getElementById("go-btn").addEventListener("click", ()=>{
  const c = document.getElementById("city-input").value.trim() || "Madrid";
  render(c);
});
document.getElementById("city-input").addEventListener("keydown", (e)=>{
  if(e.key==="Enter") document.getElementById("go-btn").click();
});

// --- Boot ---
setGreeting();
render(document.getElementById("city-input").value || "Madrid");
