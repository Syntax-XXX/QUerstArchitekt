let ws = new WebSocket("ws://" + window.location.host + "/ws");
let timerInterval;
let timeLeft = 120;

function startTimer(seconds) {
  clearInterval(timerInterval);
  timeLeft = seconds;
  updateTimer();
  timerInterval = setInterval(() => {
    timeLeft--;
    updateTimer();
    if (timeLeft <= 0) clearInterval(timerInterval);
  }, 1000);
}

function updateTimer() {
  const timerEl = document.getElementById("timerEl");
  if (!timerEl) return;
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  timerEl.innerText = `⏳ Time Left: ${mins}:${secs.toString().padStart(2, '0')}`;
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const mode = data.mode;

  const statusEl = document.getElementById("status");
  if (statusEl) {
    if (mode === "vote") {
      statusEl.innerText = "🗳️ Voting in progress...";
    } else if (mode === "quest") {
      statusEl.innerText = "🎯 Active Quest!";
    } else {
      statusEl.innerText = "💤 Add a Quest to Vote!";
    }
  }

  const ideaEl = document.getElementById("idea");
  if (ideaEl) {
    ideaEl.innerText = mode === "vote" ? `Quest Idea:\n${data.idea}` : "";
  }
  
  const questEl = document.getElementById("quest");
  if (questEl) {
    questEl.innerText = mode === "quest" ? data.quest : "";
  }

  const voteCountsEl = document.getElementById("voteCounts");
  if (mode === "vote") {
    startTimer(120);
    if (voteCountsEl) {
      voteCountsEl.style.display = "block";
      voteCountsEl.innerText = `✅ Yes: ${data.votes.yes}  ❌ No: ${data.votes.no}`;
    }
  } else if (mode === "quest") {
    if (voteCountsEl) {
      voteCountsEl.style.display = "none";
      voteCountsEl.innerText = "";
    }
    const historyEl = document.getElementById("history");
    if (historyEl && data.quest) {
      const li = document.createElement("li");
      li.textContent = data.quest.slice(0, 100) + "...";
      historyEl.prepend(li);
    }
    startTimer(1200);
  } else {
    clearInterval(timerInterval);
    if (voteCountsEl) {
      voteCountsEl.style.display = "none";
      voteCountsEl.innerText = "";
    }
    const timerEl = document.getElementById("timerEl");
    if (timerEl) timerEl.innerText = "";
  }
};

let currentOverlay = null;

async function checkOverlay() {
  try {
    const res = await fetch('/overlay/current_view.txt?_=' + new Date().getTime());
    if (!res.ok) throw new Error('Failed to fetch overlay file');
    const overlay = (await res.text()).trim();

    if (currentOverlay && overlay !== currentOverlay) {
      console.log(`Overlay changed from ${currentOverlay} to ${overlay}, reloading...`);
      location.reload();
    }
    currentOverlay = overlay;
  } catch (e) {
    console.error('Error checking overlay:', e);
  }
}

setInterval(checkOverlay, 5000);
checkOverlay();
