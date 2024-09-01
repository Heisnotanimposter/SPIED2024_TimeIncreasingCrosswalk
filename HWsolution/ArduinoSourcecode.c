#include "esp_camera.h"
#include <WiFi.h>

//
// WARNING!!! Make sure that you have either selected ESP32 Wrover Module,
//            or another board which has PSRAM enabled
//

// Select camera model
//#define CAMERA_MODEL_WROVER_KIT
//#define CAMERA_MODEL_ESP_EYE
//#define CAMERA_MODEL_M5STACK_PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE
#define CAMERA_MODEL_AI_THINKER

#include "camera_pins.h"

const char* ssid = "Dosirak055811";
const char* password = "14645905";

void startCameraServer();

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  //init with high specs to pre-allocate larger buffers
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

#if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
#endif

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  //initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1);//flip it back
    s->set_brightness(s, 1);//up the blightness just a bit
    s->set_saturation(s, -2);//lower the saturation
  }
  //drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_QVGA);

#if defined(CAMERA_MODEL_M5STACK_WIDE)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(10000);
}

void sendToArduino(String message) {
  Serial.println(message);
}

void loop() {
  // Example: Send a message to Arduino every 5 seconds
  delay(5000);
  sendToArduino("ESP32-CAM: Sending data to Arduino.");
}
// 핀 설정
const int sensorPin = A0;    // 압력 센서가 연결된 핀
const int grled = 24;       // 
const int reled = 26;

// 변수 설정
int sensorValue = 0;
int pins[] = {2,3, 4, 5, 6, 7, 8};
int C=30;
int D=31;
int num_of_pins = 7;

bool seg[6][7]=
{
  {1,0,1,1,0,1,1}, //5
  {0,1,1,0,0,1,1}, //4
  {1,1,1,1,0,0,1}, //3
  {1,1,0,1,1,0,1}, //2
  {0,1,1,0,0,0,0}, //1
  {1,1,1,1,1,1,0}, //0
};

bool segment[10][7] =
 {
  
  {1,1,1,0,0,1,1}, //9
  {1,1,1,1,1,1,1}, //8
  {1,1,1,0,0,0,0}, //7
  {1,0,1,1,1,1,1}, //6
  {1,0,1,1,0,1,1}, //5
  {0,1,1,0,0,1,1}, //4
  {1,1,1,1,0,0,1}, //3
  {1,1,0,1,1,0,1}, //2
  {0,1,1,0,0,0,0}, //1
  {1,1,1,1,1,1,0}, //0
  
};


unsigned long startTime = 0;
bool ledOn = false;



void setup() 
{ 

  for(int i=0;i<num_of_pins;++i)
  {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], HIGH);
  }
  
  pinMode(grled, OUTPUT);   // LED 핀을 출력 모드로 설정
  pinMode(reled, OUTPUT);
  pinMode(C,OUTPUT);
  pinMode(D,OUTPUT);
  Serial.begin(9600);        // 시리얼 통신 시작 (디버깅용)
}

void loop() {
  sensorValue = analogRead(sensorPin);  // 압력 센서 값 읽기
  digitalWrite(reled, 1);

  
  // 센서 값이 임계값 이상인지 확인
  if (sensorValue > 300 && !ledOn) 
  {
    if (startTime == 0) {
      startTime = millis();  // 3초 카운트 시작
    }
    
    // 3초 동안 임계값 유지 확인
    if (millis() - startTime >= 3000) 
    {
      digitalWrite(reled, LOW);
      digitalWrite(grled, HIGH);  // LED 켜기
      
      ledOn = true;
    

      for(int i=0;i<6;++i)
      {
        for(int j=0;j<7;j++)
        {
          digitalWrite(pins[j],seg[i][j]);
        }
        digitalWrite(C,1);
        digitalWrite(D,1);
        delay(1000);
      }
      for(int i=0;i<10;++i)
      {
       for(int j=0;j<7;j++)
        {
          digitalWrite(pins[j],segment[i][j]);
        }
        digitalWrite(C,0);
        digitalWrite(D,0);
        delay(1000);
      }
      
      ledOn = false;
      startTime = 0;               // 타이머 초기화
    }



  } 




  digitalWrite(grled, LOW);   // 10초 후 LED 끄기
  digitalWrite(reled, 1);
  

  

  // 시리얼 모니터에 센서 값 출력 (디버깅용)
  Serial.println(sensorValue);
  
  delay(100);  // 짧은 지연을 추가해 안정성 확보
}
void loop() {
  if (Serial.available()) {
    String incomingData = Serial.readString();
    Serial.print("Received from ESP32-CAM: ");
    Serial.println(incomingData);
  }

  // Existing loop code
  sensorValue = analogRead(sensorPin);  // Read the sensor value
  if(sensorValue > 100) { // arbitrary threshold
    digitalWrite(reled, HIGH);
    digitalWrite(grled, LOW);
  } else {
    digitalWrite(reled, LOW);
    digitalWrite(grled, HIGH);
  }

  delay(1000);
}