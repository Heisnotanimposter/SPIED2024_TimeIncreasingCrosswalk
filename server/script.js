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

    lights[currentLight].style.backgroundColor = '#111';
    currentLight = (currentLight + 1) % lights.length;
    lights[currentLight].style.backgroundColor = lights[currentLight].classList[1];

    // Get time from input or default value
    if (currentLight === 0) remainingTime = redTimeInput.value || 5;
    else if (currentLight === 1) remainingTime = yellowTimeInput.value || 2;
    else remainingTime = greenTimeInput.value || 3;

    timerDisplay.textContent = remainingTime;

    timerInterval = setInterval(() => {
        remainingTime--;
        timerDisplay.textContent = remainingTime;

        if (remainingTime === 0) {
            changeLight();
        }
    }, 1000);
}

changeLight(); // Start the sequence

// Add event listeners to inputs for real-time updates
redTimeInput.addEventListener('input', () => {
    if (currentLight === 0) {
        remainingTime = redTimeInput.value || 5;
        timerDisplay.textContent = remainingTime;
    }
});

yellowTimeInput.addEventListener('input', () => {
    if (currentLight === 1) {
        remainingTime = yellowTimeInput.value || 2;
        timerDisplay.textContent = remainingTime;
    }
});

greenTimeInput.addEventListener('input', () => {
    if (currentLight === 2) {
        remainingTime = greenTimeInput.value || 3;
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
        if (currentLight === 0) {
            remainingTime = data.redTime;
        } else if (currentLight === 1) {
            remainingTime = data.yellowTime;
        } else {
            remainingTime = data.greenTime;
        }
        timerDisplay.textContent = remainingTime;

    } catch (error) {
        console.error("Error fetching data from Google Drive:", error);
        // Handle the error gracefully (e.g., display an error message)
    }
}

// Call fetchDataFromDrive periodically or whenever you need to refresh the data
// Make sure to provide the accessToken and fileId
setInterval(() => fetchDataFromDrive(accessToken, fileId), 5000); 
