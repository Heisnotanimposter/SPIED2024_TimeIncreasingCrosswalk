# TimeIncreasingCrosswalkSPIED2024

![grandaward (1)](https://github.com/user-attachments/assets/939d5760-3630-478a-a3c9-5d03b8d8bdb5)

![IMG_2931](https://github.com/user-attachments/assets/40dd99ab-26ed-4245-a83f-273d56ad288a)

![IMG_2930](https://github.com/user-attachments/assets/3d313946-5dc4-44ad-bdf9-25e3e0baf409)

Here’s a README.md file for your project, explaining its purpose, setup, and usage.

Smart Traffic Light System with Camera Detection

Overview

This project implements a smart traffic light system using an ESP32 microcontroller. The system includes:
	•	Traffic Lights (LEDs): Controlled by the ESP32.
	•	Camera Integration: Detects pedestrians and adjusts the timer accordingly.
	•	WiFi Web Server: Hosts a basic web page for monitoring and interaction.

How It Works
	1.	The camera detects pedestrians at the crosswalk.
	2.	If a pedestrian is detected, the timer increases, allowing more time for crossing.
	3.	The system controls traffic lights (LEDs on GPIO 16 and 17).
	4.	A web interface is provided via an ESP32 web server.

Hardware Requirements
	•	ESP32 Development Board
	•	LEDs (for traffic light simulation)
	•	Resistors (as needed)
	•	Camera Module (for person detection)
	•	Power Supply (5V)

Software Requirements
	•	Arduino IDE (or PlatformIO)
	•	ESP32 Board Library
	•	WiFi Library (built-in)

Circuit Diagram

Component	ESP32 Pin
Red LED	GPIO 16
Green LED	GPIO 17
Camera	Configured via ESP32 CAM pins

Installation & Setup
	1.	Clone the repository:

git clone https://github.com/your-repository/smart-traffic-light.git


	2.	Open the code in Arduino IDE.
	3.	Install ESP32 Board Support:
	•	Go to Preferences → Add the following URL in “Additional Board Manager URLs”:

https://dl.espressif.com/dl/package_esp32_index.json


	•	Install ESP32 by Espressif Systems in the Board Manager.

	4.	Connect ESP32 to your computer via USB.
	5.	Set up WiFi credentials in the code:

const char* ssid = "your_network_name";
const char* password = "your_network_password";


	6.	Upload the code and open the Serial Monitor.

Code Breakdown
	•	WiFi Access Point Setup:
	•	ESP32 starts as a soft access point with a predefined SSID/password.
	•	Clients can connect and access a basic web page.
	•	Traffic Light Control:
	•	GPIO 16 (Red LED) and GPIO 17 (Green LED) simulate traffic lights.
	•	Future expansion: integrate a real traffic signal.
	•	Web Server Handling:
	•	Listens for HTTP requests.
	•	Displays a basic web page (Hello, World!).