const lights = document.querySelectorAll('.light');
const timerDisplay = document.getElementById('timerDisplay');
const redTimeInput = document.getElementById('redTime');
const yellowTimeInput = document.getElementById('yellowTime');
const greenTimeInput = document.getElementById('greenTime');

let currentLight = 0;
let remainingTime;
let timerInterval;

function changeLight() {
    clearInterval(timerInterval); // Clear previous timer

    // Turn off the previous light
    lights.forEach(light => light.style.backgroundColor = '#111');
    
    // Turn on the current light
    const currentClass = lights[currentLight].classList[1];
    lights[currentLight].style.backgroundColor = currentClass;

    // Set remaining time based on the current light
    if (currentClass === 'red') remainingTime = parseInt(redTimeInput.value) || 5;
    else if (currentClass === 'yellow') remainingTime = parseInt(yellowTimeInput.value) || 2;
    else remainingTime = parseInt(greenTimeInput.value) || 3;

    // Update timer display
    timerDisplay.textContent = remainingTime;

    // Start countdown
    timerInterval = setInterval(() => {
        remainingTime--;
        timerDisplay.textContent = remainingTime;

        if (remainingTime <= 0) {
            currentLight = (currentLight + 1) % lights.length; // Move to the next light
            changeLight();
        }
    }, 1000);
}

changeLight(); // Start the sequence

// Real-time updates for input fields
redTimeInput.addEventListener('input', () => {
    if (lights[currentLight].classList.contains('red')) {
        remainingTime = parseInt(redTimeInput.value) || 5;
        timerDisplay.textContent = remainingTime;
    }
});

yellowTimeInput.addEventListener('input', () => {
    if (lights[currentLight].classList.contains('yellow')) {
        remainingTime = parseInt(yellowTimeInput.value) || 2;
        timerDisplay.textContent = remainingTime;
    }
});

greenTimeInput.addEventListener('input', () => {
    if (lights[currentLight].classList.contains('green')) {
        remainingTime = parseInt(greenTimeInput.value) || 3;
        timerDisplay.textContent = remainingTime;
    }
});

// Function to fetch data from Google Drive
async function fetchDataFromDrive(accessToken, fileId) {
    try {
        const response = await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Update input fields and trigger light change if necessary
        redTimeInput.value = data.redTime;
        yellowTimeInput.value = data.yellowTime;
        greenTimeInput.value = data.greenTime;

        // If a light is currently active, update its remaining time and display
        if (lights[currentLight].classList.contains('red')) {
            remainingTime = data.redTime;
        } else if (lights[currentLight].classList.contains('yellow')) {
            remainingTime = data.yellowTime;
        } else {
            remainingTime = data.greenTime;
        }
        timerDisplay.textContent = remainingTime;

    } catch (error) {
        console.error("Error fetching data from Google Drive:", error);
    }
}

// Fetch data periodically
const accessToken = 'your-access-token'; // Set your Google Drive access token here
const fileId = 'your-file-id'; // Set your Google Drive file ID here
setInterval(() => fetchDataFromDrive(accessToken, fileId), 5000);

// Function to load the video
function loadVideo() {
    const videoElement = document.getElementById('trafficVideo');
    videoElement.src = '/Users/seungwonlee/ObjectDetection_with_Server/target/140sDayShinjuku.mp4';
    videoElement.play();
}

// Call this function once the page is fully loaded
window.onload = () => {
    loadVideo();
};

