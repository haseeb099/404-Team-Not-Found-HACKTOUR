/* Anchor — patient-facing JavaScript
 * Voice capture via Web Speech API, latency-hiding acknowledgement, audio playback.
 */

const app = document.getElementById('app');
const restingScreen = document.getElementById('resting-screen');
const responseScreen = document.getElementById('response-screen');
const responseText = document.getElementById('response-text');
const audioEl = document.getElementById('anchor-voice');
const buttons = document.querySelectorAll('#fallback-buttons button');

// --- Demo overlay: show carer notifications if ?demo=1 ---
if (new URLSearchParams(window.location.search).has('demo')) {
  document.getElementById('carer-overlay').style.display = 'block';
}

// --- Button fallback ---
buttons.forEach(btn => {
  btn.addEventListener('click', () => handleInput(btn.dataset.prompt));
});

// --- Voice input ---
let recognition = null;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-GB';

  recognition.onstart = () => app.classList.add('listening');
  recognition.onend = () => app.classList.remove('listening');
  recognition.onresult = (e) => {
    const transcript = e.results[0][0].transcript;
    handleInput(transcript);
  };
  recognition.onerror = (e) => {
    console.warn('Speech error:', e.error);
    app.classList.remove('listening');
  };
}

// Start listening when user clicks anywhere on the resting screen
restingScreen.addEventListener('click', () => {
  if (recognition && !app.classList.contains('speaking')) {
    recognition.start();
  }
});

// Auto-start listening every time a response finishes
audioEl.addEventListener('ended', () => {
  setTimeout(() => {
    showResting();
    if (recognition) recognition.start();
  }, 400);
});


async function handleInput(text) {
  if (!text || !text.trim()) return;

  // LATENCY HIDE: play instant acknowledgement while LLM + TTS generate
  playAcknowledgement();

  try {
    const res = await fetch('/api/speak', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text})
    });
    const data = await res.json();
    showResponse(data.response_text);
    if (data.audio_url) {
      audioEl.src = data.audio_url;
      audioEl.play();
    } else {
      // Browser TTS fallback
      const utter = new SpeechSynthesisUtterance(data.response_text);
      utter.rate = 0.95;
      utter.pitch = 1.0;
      utter.onend = () => audioEl.dispatchEvent(new Event('ended'));
      speechSynthesis.speak(utter);
    }
  } catch (err) {
    console.error(err);
    showResponse("I'm having a little trouble — let's try again in a moment.");
  }
}

// Pre-loaded acknowledgement — a soft "mmm" or breath, ~500ms
// In production, replace with a real audio file at /static/assets/ack.mp3
const ackAudio = new Audio('/static/assets/ack.mp3');
ackAudio.volume = 0.5;
function playAcknowledgement() {
  ackAudio.currentTime = 0;
  ackAudio.play().catch(() => { /* ignore autoplay policy errors */ });
}

function showResponse(text) {
  responseText.textContent = text;
  responseScreen.hidden = false;
  app.classList.add('speaking');
}

function showResting() {
  app.classList.remove('speaking');
  setTimeout(() => { responseScreen.hidden = true; }, 600);
}