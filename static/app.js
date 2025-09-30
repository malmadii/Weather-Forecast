console.log("App JS loaded.");

function iconUrl(code){ return `https://openweathermap.org/img/wn/${code}@2x.png`; }

async function getCurrent(city){
  const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
  console.log("GET /api/weather status", res.status);
  return res.json();
}

async function renderCurrent(city){
  console.log("renderCurrent()", city);
  try{
    const data = await getCurrent(city);
    console.log("API payload:", data);
    if(data.error){ alert(data.error); return; }

    document.getElementById("city-name").textContent = data.city;
    document.getElementById("current-desc").textContent = data.description;
    document.getElementById("temp").textContent = `${data.temp}°C`;
    const img = document.getElementById("icon");
    img.src = iconUrl(data.icon);
    img.alt = data.description || "weather icon";
  }catch(err){
    console.error("render error", err);
    alert("Failed to fetch weather.");
  }
}

// greeting
(function greeting(){
  const h = new Date().getHours();
  const g = h<12?"Good Morning":(h<18?"Good Afternoon":"Good Evening");
  document.getElementById("greeting").textContent = `${g}, Mona!`;
})();

// search handlers
document.getElementById("go-btn").addEventListener("click", ()=>{
  const c = document.getElementById("city-input").value.trim() || "Madrid";
  renderCurrent(c);
});
document.getElementById("city-input").addEventListener("keydown", (e)=>{
  if(e.key==="Enter") document.getElementById("go-btn").click();
});

// initial render
renderCurrent("Madrid");
