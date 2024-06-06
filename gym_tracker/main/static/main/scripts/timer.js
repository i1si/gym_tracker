let timer = document.getElementById('timer');
let startBtn = document.getElementById('startBtn');
let pauseBtn = document.getElementById('pauseBtn');
let resetBtn = document.getElementById('finishBtn');

let seconds = 0;
let minutes = 0;
let hours = 0;
let interval;


function sendRunningStats() {
    function IsNumeric(input){
        return (input - 0) == input && (''+input).trim().length > 0;
    };
    let distance = document.getElementById('distance').value;
    if (IsNumeric(distance)) {
        let duration = seconds + minutes * 60 + hours * 3600;
        let data = {
            "distance": distance,
            "duration": duration
        };
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(window.location.origin + '/api/v1/runnings/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json;charset=utf-8'
            },
            mode: "same-origin"
        })
        window.location.replace(document.location.origin)
    } else {
        document.getElementById('distance').classList.add('is-invalid')
        document.getElementById('validationError').textContent = 'Введите целое число'
    }
}

function updateTime() {
    seconds++;
    if (seconds === 60) {
        minutes++;
        seconds = 0;
    }
    if (minutes === 60) {
        hours++;
        minutes = 0;
    }
    timer.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

startBtn.addEventListener('click', () => {
    interval = setInterval(updateTime, 1000);
    startBtn.classList.add('disabled');
    finishBtn.classList.remove('disabled');
});

finishBtn.addEventListener('click', () => {
    clearInterval(interval);
    finishBtn.classList.add('disabled');
});

