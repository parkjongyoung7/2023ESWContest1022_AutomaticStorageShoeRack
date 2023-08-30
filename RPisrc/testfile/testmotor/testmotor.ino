
int insert_IRsensor=4;
int Diode_sensor=2;
int PUL_PIN=7;
int DIR_PIN=8;
int speaker=3;
int remove_IRsensor=9;
String Data="";

int melody[] ={349, 0, 294, 0, 294,294,294,0,294, 0, 349,294,233,0,294,0,349,294,
294,0,233,233,233,0,349,0,349,0,349,294,233,0,294,0,233,294,233,294,349};
void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
  pinMode(insert_IRsensor,INPUT); 
  pinMode(Diode_sensor, INPUT);
  pinMode(PUL_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(speaker,OUTPUT);
  pinMode(remove_IRsensor,INPUT);
  
}

void insert_scenario(){
  //RPi에게 수납시나리오를 시작하라는 신호를  보냄
  Serial.println("Insert");
  //Data는 RPi에게 받을 메세지를 저장하기 위한 문자열
  String Data="";
  //아래 loop는 모터를 움직이기 전 신발이 정렬되있나 확인하는 과정이다
  while(1) 
  {
    delay(2000);
    //RPi는 찍은 사진을 바탕으로 3가지 메세지를 보낸다
    if (Serial.available()) {
          Data = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
          Data.trim();  //개행문자 제거
    }
    int val=digitalRead(insert_IRsensor);
    //신발이 정렬되지 않았거나 발판 밖으로 삐져나왔다면 스피커 알림
    if (Data=="sort please" ) {
          for (int i = 0; i < 39; i++)
            {
             tone(speaker, melody[i], 250);
             delay(250);
             noTone(8);
             }
         }

    
    //신발이 없다면(수납부 IR센서가 오동작했다면) 시나리오를 종료
    if (Data=="no shoe") {
          
          return ;
    }
    val=digitalRead(insert_IRsensor);
    if (Data=="ok"){
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
        break;
      }
     
    }
    //아래의 경우는 스티커를 모두 가렸으나 IR sensor가 인식되어 소리가 났을 때
    //RPi코드는 이미 move motor를 보내버린다
    //따라서 이런 상황에서 Data에는 move motor가 저장되어있고 loop을 탈출하기 위해 
    //아래와 같은 코드를 넣었다
    if (Data=="move motor") {
          break;
       }
  }
  // classification 과정 생략
  //RPi로부터 모터를 움직이라는 신호를 기다림
   while(1) 
    {
      if (Serial.available()) {
          Data = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
          Data.trim();  //개행문자 제거
          
       }
       
       if (Data=="move motor") {
          break;
       }
    }
    
    //다이오드 센서가 인식 될 때까지 모터를  움직인다.
    //실제로는 움직이는 각을 정하고 마지막에 다이오드를 센서를 확인하지만
    //이번 test에서는 다이오드센서가 인식했을 때 모터가 얼마나 빨리 반응하나를 확인할 것임

    while (1) {
        digitalWrite(PUL_PIN, HIGH);
        delayMicroseconds(500);
        
        digitalWrite(PUL_PIN,LOW); // delay(1) 이상 하지말것. 모터죽음
     
        delayMicroseconds(500);
        if (digitalRead(Diode_sensor)==HIGH){
          break;
        }
      
    }
    
     
    //모터 움직임이 끝났다고 RPi에게 알림delay(1);
    Serial.println("Done");
    //RPi가 종료되었다고 알림. 시나리오 종료는 RPi 먼저함
    while(1) {
       if (Serial.available()) {
          Data = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
          Data.trim();  //개행문자 제거
          
       }
       if (Data=="Done") {
          break;
       }
    }
  
  
}

void remove_scenario() {
  int 
}

void loop() {
  int val=0;
  
  val = digitalRead(insert_IRsensor);

  if (val==LOW) {
    insert_scenario();
        
  } 
  //RPi가 아두이노로부터 데이터를 받아들이는 함수는
  //데이터를 받아들일 때까지 대기함
  //RPi의 코드를 돌리기 위해 trivial 값을 보냄
  Serial.println(".\n");
  if (Serial.available()) {
         Data = Serial.readStringUntil('\n'); // 개행문자까지 읽어드림
         Data.trim();  //개행문자 제거
         int angle=atoi(Data);
         //motor 돌리는 코드
          delay(2000);
          while () {
            
          }
         Serial.println(angle);
                          }
  
  delay(1000);
}
