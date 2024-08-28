#include <WiFi.h>

// Network credentials Here
const char* ssid     = "yunet";
const char* password = "yYSjA28x";

// Set web server port number to 80
WiFiServer server(80);

// Variable to store the HTTP request
String header;

// Output variable to GPIO pins
const int ledPin16 = 16;
const int ledPin17 = 17;

void setup() {
    Serial.begin(115200);

    // Initialize GPIO pins
    pinMode(ledPin16, OUTPUT);
    pinMode(ledPin17, OUTPUT);
    digitalWrite(ledPin16, LOW);  // Set initial state to LOW
    digitalWrite(ledPin17, LOW);  // Set initial state to LOW

    // Start Wi-Fi as an access point
    WiFi.softAP(ssid, password);
    Serial.println("Web Server started. IP address:");
    Serial.println(WiFi.softAPIP());

    // Start the server
    server.begin();
}

void loop() {
    WiFiClient client = server.available();   // Listen for incoming clients

    if (client) {                             // If a new client connects,
        Serial.println("New Client.");        // print a message out in the serial port
        String currentLine = "";              // make a String to hold incoming data from the client

        while (client.connected()) {          // loop while the client's connected
            if (client.available()) {         // if there's bytes to read from the client,
                char c = client.read();       // read a byte, then
                Serial.write(c);              // print it out the serial monitor
                header += c;
                if (c == '\n') {              // if the byte is a newline character
                    // if the current line is blank, you got two newline characters in a row.
                    // that's the end of the client HTTP request, so send a response:
                    if (currentLine.length() == 0) {
                        // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
                        // and a content-type so the client knows what's coming, then a blank line:
                        client.println("HTTP/1.1 200 OK");
                        client.println("Content-type:text/html");
                        client.println("Connection: close");
                        client.println();

                        // Display the HTML web page
                        client.println("<html><body><h1>Hello, World!</h1></body></html>");
                        client.println();

                        // The HTTP response ends with another blank line
                        break;
                    } else {
                        currentLine = "";
                    }
                } else if (c != '\r') {
                    currentLine += c;      // add it to the end of the currentLine
                }
            }
        }
        // Clear the header variable
        header = "";
        // Close the connection
        client.stop();
        Serial.println("Client disconnected.");
    }
}
