
// ====== CONFIG ======
const BASE_URL = localStorage.getItem('fitmantra_api') || 'http://127.0.0.1:5000';

// Helpers
const qs = s => document.querySelector(s);
const qsa = s => Array.from(document.querySelectorAll(s));

// Smooth scroll
qs('#startBtn').addEventListener('click', () => {
  document.getElementById('chatbot').scrollIntoView({behavior:'smooth'});
});

// Chatbot
qs('#sendBtn').addEventListener('click', sendMessage);
qs('#user-input').addEventListener('keydown', e => { if(e.key==='Enter'){ sendMessage(); }});

async function sendMessage() {
  const inputEl = qs('#user-input');
  const chat = qs('#chat-window');
  const text = (inputEl.value || '').trim();
  if(!text) return;
  chat.insertAdjacentHTML('beforeend', `<p><b>You:</b> ${text}</p>`);
  inputEl.value='';

  try {
    const res = await fetch(`${BASE_URL}/chatbot`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message:text})
    });
    const data = await res.json();
    chat.insertAdjacentHTML('beforeend', `<p><b>FitMantra Bot:</b> ${data.response}</p>`);
    chat.scrollTop = chat.scrollHeight;
  } catch (e) {
    chat.insertAdjacentHTML('beforeend', `<p class="muted">Error talking to server.</p>`);
  }
}

// Plan
qs('#loadPlanBtn').addEventListener('click', loadPlan);
async function loadPlan(){
  const container = qs('#plan-container');
  container.innerHTML = '<p class="muted">Loading...</p>';
  try{
    const res = await fetch(`${BASE_URL}/fitness-plan`);
    const data = await res.json();
    container.innerHTML = '';
    data.forEach(row => {
      const day = row.Day || row.day || row['DAY'] || 'Day';
      const workout = row.Workout || row.workout || row['WORKOUT'] || '';
      container.insertAdjacentHTML('beforeend', `<div class="day"><h3>${day}</h3><p>${workout}</p></div>`);
    });
  }catch(e){
    container.innerHTML = '<p class="muted">Unable to load plan.</p>';
  }
}

// Progress
qs('#progress-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const user = qs('#user').value.trim();
  const workout = qs('#workout').value.trim();
  const date = qs('#date').value;
  if(!user || !workout || !date){ return; }
  try{
    await fetch(`${BASE_URL}/progress`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({user, workout, date})
    });
    qs('#progress-message').textContent = '✅ Progress saved!';
    loadProgress();
    e.target.reset();
  }catch(err){
    qs('#progress-message').textContent = 'Error saving progress.';
  }
});

async function loadProgress(){
  try{
    const res = await fetch(`${BASE_URL}/get-progress`);
    const data = await res.json();
    const tbody = qs('#progress-table tbody');
    tbody.innerHTML = '';
    data.forEach(r => {
      tbody.insertAdjacentHTML('beforeend', `<tr><td>${r.user}</td><td>${r.workout}</td><td>${r.date}</td></tr>`);
    });
  }catch(e){ /* ignore */ }
}
loadProgress();
