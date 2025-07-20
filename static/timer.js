let timeLeft = 25 * 60;
let timer;
let isRunning = false;

function updateDisplay() {
    const min = Math.floor(timeLeft / 60);
    const sec = timeLeft % 60;
    document.getElementById('display').textContent =
        `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
}

function startTimer() {
    if (!isRunning) {
        timer = setInterval(() => {
            timeLeft--;
            updateDisplay();
            if (timeLeft <= 0) {
                clearInterval(timer);
                alert("Pomodoro Complete!");
                isRunning = false;
            }
        }, 1000);
        isRunning = true;
    }
}

function resetTimer() {
    clearInterval(timer);
    timeLeft = 25 * 60;
    updateDisplay();
    isRunning = false;
}

updateDisplay();
