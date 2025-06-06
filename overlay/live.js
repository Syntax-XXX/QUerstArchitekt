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
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  document.getElementById("timer").innerText = `⏳ Time Left: ${mins}:${secs.toString().padStart(2, '0')}`;
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const mode = data.mode;
  document.getElementById("status").innerText = mode === "vote" ? "🗳️ Voting in progress..." : "🎯 Active Quest!";
  document.getElementById("idea").innerText = mode === "vote" ? `Quest Idea:
${data.idea}` : "";
  document.getElementById("quest").innerText = mode === "quest" ? data.quest : "";

  if (mode === "vote") {
    startTimer(120);
    document.getElementById("voteCounts").innerText = `✅ Yes: ${data.votes.yes}  ❌ No: ${data.votes.no}`;
    setTimeout(() => {
    window.location.reload();
  }, 5000);
  } else if (mode === "quest") {
    const li = document.createElement("li");
    li.textContent = data.quest.slice(0, 100) + "...";
    document.getElementById("history").prepend(li);
    startTimer(1200);
    document.getElementById("voteCounts").innerText = "";
    setTimeout(() => {
    window.location.reload();
  }, 5000);
  } else {
    document.getElementById("timer").innerText = "";
    clearInterval(timerInterval);
    document.getElementById("voteCounts").innerText = "";
  }
};
