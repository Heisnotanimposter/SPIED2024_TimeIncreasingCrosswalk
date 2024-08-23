const lights = document.querySelectorAll('.light');
const timerDisplay = document.getElementById('timerDisplay');
const redTimeInput = document.getElementById('redTime');
const yellowTimeInput = document.getElementById('yellowTime');
const greenTimeInput = document.getElementById('greenTime');

let currentLight = 0;
let remainingTime;
let timerInterval;

// Dynamic timer adjustment based on traffic conditions
function adjustTimers(vehicleCount, personCount, personSpeed) {
    let baseGreenTime = 30;  // Base time for green light
    let baseRedTime = 30;    // Base time for red light

    // Adjust green light duration based on vehicle and person counts
    if (vehicleCount > personCount) {
        baseGreenTime -= Math.min(vehicleCount, 10);  // Reduce green time by up to 10 seconds
    } else {
        baseGreenTime += Math.min(personCount, 10);  // Increase green time by up to 10 seconds
    }

    // Adjust red light duration based on person speed
    if (personSpeed > 6) {  // Assume 6 km/h is the average walking speed
        baseRedTime -= Math.min(personSpeed - 6, 10);  // Reduce red time by up to 10 seconds
    } else {
        baseRedTime += Math.min(6 - personSpeed, 10);  // Increase red time by up to 10 seconds
    }

    greenTimeInput.value = baseGreenTime;
    redTimeInput.value = baseRedTime;
}

function changeLight() {
    clearInterval(timerInterval); // Clear previous timer

    lights[currentLight].classList.remove('red', 'green', 'yellow');
    lights[currentLight].classList.add('off');
    currentLight = (currentLight + 1) % lights.length;
    lights[currentLight].classList.remove('off');
    lights[currentLight].classList.add(lights[currentLight].classList[1]);

    // Get time from input or default value
    if (currentLight === 0) remainingTime = parseInt(redTimeInput.value) || 30;
    else if (currentLight === 1) remainingTime = parseInt(yellowTimeInput.value) || 3;
    else remainingTime = parseInt(greenTimeInput.value) || 30;

    timerDisplay.textContent = remainingTime;

    timerInterval = setInterval(() => {
        remainingTime--;
        timerDisplay.textContent = remainingTime;

        if (remainingTime === 0) {
            changeLight();
        }
    }, 1000);
}

function updateTrafficData() {
    fetch('/counts')
        .then(response => response.json())
        .then(data => {
            const vehicleCountA = data.vehicle_count.Aphase;
            const personCountA = data.person_count.Aphase;
            const personSpeedA = data.person_speed.Aphase || 6; // Default to 6 km/h if not available

            adjustTimers(vehicleCountA, personCountA, personSpeedA);

            document.getElementById('vehicle_count_a').innerText = vehicleCountA;
            document.getElementById('vehicle_count_b').innerText = data.vehicle_count.Bphase;
            document.getElementById('person_count_a').innerText = personCountA;
            document.getElementById('person_count_b').innerText = data.person_count.Bphase;
        });
}

changeLight(); // Start the sequence

// Update traffic data every second
setInterval(updateTrafficData, 1000);

// Add event listeners to inputs for real-time updates
redTimeInput.addEventListener('input', () => {
    if (currentLight === 0) {
        remainingTime = parseInt(redTimeInput.value) || 30;
        timerDisplay.textContent = remainingTime;
    }
});

yellowTimeInput.addEventListener('input', () => {
    if (currentLight === 1) {
        remainingTime = parseInt(yellowTimeInput.value) || 3;
        timerDisplay.textContent = remainingTime;
    }
});

greenTimeInput.addEventListener('input', () => {
    if (currentLight === 2) {
        remainingTime = parseInt(greenTimeInput.value) || 30;
        timerDisplay.textContent = remainingTime;
    }
});
