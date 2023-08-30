#include <Adafruit_NeoPixel.h>

int insert_IRsensor=5;   //수납부 적외선 센서
int Diode_sensor=4;     //다이오드센서
int PUL_PIN=11;          //모터 신호 핀
int DIR_PIN=12;          //모터 방향 핀
int speaker=2;          //스피커
int remove_IRsensor=3;  //출납무 적외선 센서
int NEO_PIN=8;          //LED 핀
int LED_PIXEL=12;      //LED 픽셀 수
String Data="";

boolean isScenarioRunning = false;

int melody[] ={349, 0, 294, 0, 294,294,294,0,294, 0, 349,294,233,0,294,0,349,294,
294,0,233,233,233,0,349,0,349,0,349,294,233,0,294,0,233,294,233,294,349};
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(LED_PIXEL,NEO_PIN,NEO_GRB + NEO_KHZ800);
void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
  pinMode(insert_IRsensor,INPUT); 
  pinMode(Diode_sensor, INPUT);
  pinMode(PUL_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(speaker,OUTPUT);
  pinMode(remove_IRsensor,INPUT);
  pixels.begin(); //네오픽셀 초기화
  pixels.setBrightness(180); // 밝기설정 //최대 255  
  off_led();//led 끄기
}
//LED on
void on_led(){
  for (int i = 0; i < LED_PIXEL; i++) {
    pixels.setPixelColor(i, 255, 255, 255);
}
  pixels.show();
}
//LED off
void off_led(){
  for (int i = 0; i < LED_PIXEL; i++) {
    pixels.setPixelColor(i, 0, 0, 0);
  }
  pixels.show();
}

// 모터 회전각 인자로 받아 모터 움직이는 함수
void move_motor(int DIR, int d ) {
    int correct=0;
    //CW
    if (DIR==0) {
      digitalWrite(DIR_PIN,LOW);
    }
    //CCW
    else {
      digitalWrite(DIR_PIN,HIGH);
    }

    for (int i=0; i<700*d;i++) {
      digitalWrite(PUL_PIN,HIGH);
      delayMicroseconds(2000);
      digitalWrite(PUL_PIN,LOW);
      delayMicroseconds(2000);
    }
    while (correct==0){
      digitalWrite(PUL_PIN,HIGH);
      delayMicroseconds(2000);
      digitalWrite(PUL_PIN,LOW);
      delayMicroseconds(2000);
      correct=digitalRead(Diode_sensor);
    }
}


// 라즈베리파이에서 회전각, 방향 받아 움직임 명령 내리는 함수
void motor_data_check(){
  //모터 각을 받기 위한 변수
  String Data_motor="";
  while(1){
    if (Serial.available()){
     Data_motor = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
     Data_motor.trim();
    }  //개행문자 제거
    //
    if (Data_motor == "CW1"){
      move_motor(0,1);
      break;
    }
    else if (Data_motor=="CCW1"){
      move_motor(1,1);
      break;
    }
    else if(Data_motor=="CCW2"){
      move_motor(1,2);
      break;
    }
    else if (Data_motor=="stay"){
      break;      
    }
  }
}


void insert_scenario(){
  isScenarioRunning = true;

  //RPi에게 수납시나리오를 시작하라는 신호를  보냄
  on_led();
  Serial.println("Insert");
  //Data는 RPi에게 받을 메세지를 저장하기 위한 문자열
  String Data_insert="";
  //아래 loop는 모터를 움직이기 전 신발이 정렬되있나 확인하는 과정이다
  while(1) 
  {
    delay(2000);
    //RPi는 찍은 사진을 바탕으로 3가지 메세지를 보낸다
    if (Serial.available()) {
          Data_insert = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
          Data_insert.trim();  //개행문자 제거
    }
    int val=digitalRead(insert_IRsensor);
    //신발이 정렬되지 않았거나 발판 밖으로 삐져나왔다면 스피커 알림
    if (Data_insert=="sort please" ) {
          for (int i = 0; i < 8; i++)
            {
             tone(speaker, melody[i], 250);
             delay(250);
             noTone(8);
             }
         }

    
    //신발이 없다면(수납부 IR센서가 오동작했다면) 시나리오를 종료
    if (Data_insert=="no shoe") {
          off_led();
          isScenarioRunning = false;
          return ;
    }
    val=digitalRead(insert_IRsensor);
    if (Data_insert=="ok"){
      //신발이 2개 인식되었지만 삐져나온 경우
      if (val==LOW) 
      {
        for (int i = 0; i < 39; i++) 
        {
             tone(speaker, melody[i], 250);
             delay(250);
             noTone(8);
        }
      }
      else 
      {
        off_led();
        break;
      }
     
    }
    
  }
  // 라즈베리파이에 모터 움직일 준비 됐다고 신호 보냄
  Serial.println("Ready");
  // 라즈베리파이에서 모터 회전각 받아 움직임
  motor_data_check();
  


     
  //모터 움직임이 끝났다고 RPi에게 알림delay(1);
  Serial.println("Done");
  //RPi가 종료되었다고 알림. 시나리오 종료는 RPi 먼저함
    while(1) {
      if (Serial.available()) {
        Data_insert = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
        Data_insert.trim();  //개행문자 제거
      }
      if (Data_insert=="Done") {
        break;
      }
    }
  
  isScenarioRunning = false;
  return;
}



void remove_scenario() {
  isScenarioRunning = true;

  int IR=0;
  String Data_remove="";
  motor_data_check();
  Serial.println("Done");
  while(1){
    if (Serial.available()) {
      Data_remove = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
      Data_remove.trim();
    }
    if (Data_remove=="DatabaseDone") {
      break;
    }
  }
  while (1){
    IR=digitalRead(remove_IRsensor);
    if (IR==0) {
      while (1){
        IR=digitalRead(remove_IRsensor);
        if (IR == 1){
          break;
        }
      }
    }
    else{
      continue;
    }
      
    break;
  }
  delay(1000);
  Serial.println("FindEmpty");
  motor_data_check();
  delay(1000);
  Serial.println("Done");
  while(1){
    if (Serial.available()) {
      Data_remove = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
      Data_remove.trim();
    }
    if (Data_remove=="DatabaseDone") {
      break;
    }
  }
  isScenarioRunning = false;
}

void loop() {
  int val_IR=1;
  
  val_IR = digitalRead(insert_IRsensor);

  if (val_IR==LOW) {
    if (isScenarioRunning == false){
      insert_scenario();
    }
        
  } 
  //RPi가 아두이노로부터 데이터를 받아들이는 함수는
  //데이터를 받아들일 때까지 대기함
  //RPi의 코드를 돌리기 위해 trivial 값을 보냄
  Serial.println(".\n");
  if (Serial.available()) {
         Data = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
         Data.trim();  //개행문자 제거
         if (Data == "remove_scenario" && isScenarioRunning == false){
           remove_scenario();
         }
        
          
         
                          }
  
  delay(1000);
}
