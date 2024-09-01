#include <SoftwareSerial.h>
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
SoftwareSerial hc06(10, 11);

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
   Serial.begin(115200); // Arduino 시리얼 모니터 시작
  hc06.begin(115200);

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

   if (hc06.available()) {
    String receivedData = hc06.readString(); // 수신된 데이터 읽기
    Serial.println("Received: " + receivedData); // 시리얼 모니터에 수신된 데이터 출력
  }
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