# ESE2023_AutomaticStorageShoeRack

# 신발 정리해조 - 자동 수납 신발장
-----------------
# Project Introduction
 본 프로젝트에서는 집에 들어갈 때 편리하게 신발을 자동으로 수납해주는 자동 정리 신발장 제작을 목표로 한다.   현관이 협소한 1인 가구 거주자를 대상으로 하며, 정해진 수납 위치에 신발을 넣으면 자동으로 정리한 후, 집에서 나갈 때는 사용자가 원하는 신발을 출납 위치에서 꺼내갈 수 있도록 한다. 스마트폰 어플리케이션을 통해 나갈 때 신을 신발을 미리 선택하고, 신발을 관리할 수 있는 기능을 제공한다. 자취방의 현관은 공간이 협소해 신발을 정리하기에 어려움이 있다. 정리를 안하다보면 신발이 섞이고 원하는 신발을 찾기가 어려워진다. 자동 정리 신발장은 이런 고초를 겪는 자취생들의 고민을 해결해줄 것으로 예상된다. 정해진 수납 위치에만 넣으면 자동으로 정리해준다. 또한 앱을 통해 신발을 관리하고 출납하여 보다 쉽게 신발을 찾을 수 있도록 도와준다. 이러한 기능을 구현하기 위해 아래와 같이 소프트웨어를 설계하였다. 

------------------  

# Architecture

## 목적 개통도
![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/ff1e2288-f86e-4b92-ae81-dd93fd2d81ce)

### 실용성
 자동정리 신발장이 실용적이기 위해서는 하드웨어 동작이 정확하고 수납/출납에 대한 시나리오가 빠르게 동작해야 한다. 스텝모터를 사용하기 때문에 발판의 움직임을 정확하게 제어할 수 있다. 신발이 발판 위에 불안정하게 놓여있으면 떨어질 염려가 있다. 불안정하게 놓여있는 신발을 제대로 놓여있을 때까지 하드웨어의 동작은 시작하지 않는다. 이처럼 시나리오가 지연되는 것을 막기 위해 사용자에게 스피커로 신발이 제대로 놓여있지 않음을 알린다.

### 편의성
 자동 정리 신발장은 사용자에게 편리함을 제공한다. 수납하는 발판의 위치를 아래쪽으로 두어 사용자가 손을 이용하지 않고 발로 신발을 넣을 수 있게 한다. 또한, 출납위치를 위쪽에 둠으로써 출납할 신발과 사용자의 손이 최대한 가깝게 한다. 사용자는 스마트폰의 앱을 이용함으로써 간단히 신발의 리스트를 확인하고 관리할 수 있다. 라즈베리파이와 앱은 신발의 데이터를 firebase를 통해 처리하기 때문에 사용자가 어떠한 IP주소이든 간에 산발 데이터에 대한 접근과 수정을 할 수 있다. Classification을 활용해 수납한 신발을 분류하여 자동으로 리스트에 신발이 업데이트될 수 있도록 한다. 또한, 새로운 종류/색깔의 신발을 인식했을 경우 앱을 통해 새로운 신발을 리스트에 등록할 수 있다.

### 경제성 
 주요 타겟이 자취방에 사는 자취생들이기 때문에 실용성과 편의성을 최대한 보장하는 선에서 재료비를 최소화한다.
 

## 시스템 개략도
![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/cf9a9a5a-c97e-4f78-8f16-75b7f52589fd)

 제품 형태 및 시스템 개략도는 위와 같다. 전체적인 시스템을 자동 신발 수납장(제어부), 데이터베이스, 스마트폰 어플리케이션으로 나눌 수 있다. 자동 신발 수납장은 아두이노를 중심으로 한 입출력 장치와, 아두이노에서 받은 제어 신호를 기반으로 신발 상태에 대한 판단을 수행하는 라즈베리파이로 구성된다. 어플리케이션은 사용자가 신발 상태를 확인하고 신발장에 대한 조작 명령을 받아 처리한다. 데이터베이스는 신발 정보를 저장하여 어플리케이션과 수납장 사이에서 정보를 송수신하는 매개체로 사용된다.

## 회로 구현 
 ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/b1649098-190d-4dfc-b828-514b1d17b97c)
 
 위 사진은 전원은 생략한 아두이노 회로도이다. 모터드라이버는 사진과 실제가 약간 다르나 사용하는 핀의 역할은 모두 동일하다. 각 센서의 역할은 다음과 같다.
 
 - 모터 드라이버 – PUL pin의 on/off 주기를 조절하여 스텝모터를 동작시키고, DIR 핀은 모터의 회전 방향을 설정한다
 
 - 스피커 –신발이 한짝만 올라왔을 경우 사용자에게 경고음을 내보낸다.
 
 - 수납 적외선 센서 – 사용자가 신발을 넣을 때 인식되고 이 센서값을 보고 판단하여 수납시나리오를 시작한다. 추가로 신발이 삐져나왔는지 감지한다.
 
 - 출납 적외선 센서 – 출납 시나리오가 진행될 때, 출납할 신발을 사용자가 가져갔는지 확인한다.
 
 - 네오픽셀 led – 수납시나리오가 진행될 때,카메라 동작환경이 어둡기 때문에 classification과 detection을 잘하기 위하여 사용한다.
 
 - 다이오드 센서 – 발판의 위치가 정확하게끔, 즉 모터의 회전수를 컨트롤하는 역할을 한다.

------------------

# Scenario
![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/af87580c-9764-437b-b9b0-cb3402b1b274)

## 수납 시나리오
 사용자가 신발을 수납부에 넣으면 옆에 있는 적외선 센서가 이를 감지한다. 아두이노가 정보를 받아 라즈베리 파이와 연결된 카메라가 수납부의 사진을 찍고 이를 분석한다. Detection 과정에서 신발이 잘 올라갔는지 opencv 이미지처리를 사용하여 확인한다. 만약 신발의 일부만 올라가면 잘못 올라간 것으로 판단하여 아두이노와 연결된 스피커에서 에러 효과음을 출력한다. 정상적으로 신발이 올라가 있는 것이 확인되면, 신발 종류와 색상을 파악한다. 신발 판단 결과가 기존 리스트에 있는 신발이라면 별도의 푸시알림 없이 수납 시나리오를 진행한다. 리스트에 없는 경우, 앱에게 신발의 사진과 함께 새로운 신발인지 묻는 푸시알림을 보낸다. 푸시알림을 보내는 이유는 인공지능 판단의 오작동을 방지하기 위해 사용자가 2차 검증을 할 수 있도록 하기 위해서 알림 기능을 추가하였다. 선택 후 기기는 신발을 보관하고 새로운 수납 발판을 제공하기 위해 모터를 작동한다. 불필요한 작동과 에너지 소모를 줄이기 위해 최단 거리에 있는 빈 발판을 수납부에 위치시킨다. 그 후 발판별 신발의 정보를 갱신하고 수납 시나리오를 종료한다.
 
## 출납 시나리오

 사용자는 사용을 원하는 신발을 어플 내에서 출납 버튼을 눌러 출납을 요청하면 파이어베이스에서 신발에 해당하는 문서 이름으로 필드가 변경되고, 라즈베리파이는 그 필드값을 불러와 해당 신발의 발판 정보를 데이터베이스에서 검색하여 가져온다. 라즈베리파이에서 계산한 출납부까지 도달하기 위한 모터 회전각을 아두이노가 전달받아 모터를 돌려 요청한 신발을 출납부에 위치시킨다. 사용자가 신발을 꺼내면 센서가 이를 감지하고, 수납부에 위치한 발판이 비었는지 판별하고 비어있지 않으면 빈 발판을 제공하기 위해 모터가 계산한 회전각만큼 회전한다.

------------------

# Software Design
 위의 시스템 구조, 시나리오를 바탕으로 다음과 같이 소프트웨어를 다음과 같이 설계하였다.
 ## 신발 detection 및 분류 과정
 
 
 ### 신발 detection 
  ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/bb9da1ba-8774-47e7-b810-c9ead79071fc)
  
  신발의 개수를 파악하기 위해 발판에 10개의 노란 색 스티커를 부착하고, 카메라로 촬영한 이미지에서 노란색 스티커의 개수를 감지하여 신발이 몇 개 올라가 있는지 파악한다. 감지 방법은 노란색의 범위를 지정하여 opencv 알고리즘을 통해 노란색 부분의 mask를 추출해 contour를 생성하고, contour의 개수를 리턴한다. 신발이 없을 경우는 그림 (a)에서 10개의 스티커가 모두 감지되고, 신발이 1짝일 경우는 그림 (b)에서 4개의 스티커가 감지된다. 그리고 신발이 2짝으로 올바르게 올라갈 경우 그림 (c)에서 모든 스티커가 가려 0개가 감지된다.
  
 신발에 노란색 무늬가 존재할 경우 이것을 스티커로 인식하여 오동작을 일으킬 위험성이 있다. 이를 방지하기 위해 색상뿐만 아니라 contour의 넓이와 모양 또한 고려하기로 하였다. 똑같은 크기와 모양의 스티커를 바닥에 부착하고, 사전에 스티커의 크기를 계산하여 범위 내에 있는 경우만 인식한다. 모양의 경우 두 contour의 모양 일치 정도를 계산하는 cv2.matchShapes 함수를 사용한다. 사전에 바닥에 부착된 스티커 1장에서 contour를 뽑아내어 촬영한 신발 사진의 contour와의 모양 불일치 정도(distance)를 계산하여 임계값보다 낮을 경우만 카운트한다.

### 신발 분류
 
 #### 신발 종류 구분

이번 프로젝트에서 여러 개의 신발 종류를 구분해내야 하므로 class가 여러 개인 Multi-class classification을 수행한다. 데이터셋으로는 kaggle의 [Large Shoe Dataset](https://www.kaggle.com/datasets/aryashah2k/large-shoe-dataset-ut-zappos50k)의 /ut-zap50k-images 폴더 내의 이미지를 활용하여 우리가 분류하고자 하는 구두, 스니커즈, 슬리퍼로 다시 나누었다. 구두의 경우 /Shoes의 Loafers, Oxfords 폴더에서, 스니커즈의 경우 /Shoes의 /Sneakers and Athletic Shoes 폴더에서, 슬리퍼의 경우 /Sandals의 Flat 폴더와 /Slippers의 Slipper Flats 폴더에서 이미지를 가져왔다.
앞에서 설명한 폴더 내의 이미지를 확인한 결과, 위 그림과 같이 우리가 예상한 신발 모양과는 달라 학습에 방해가 될 것으로 예상되는 이미지를 선별하는 작업을 수작업으로 진행하였다. 선별한 데이터셋을 train:valid:test = 6:2:2로 나누고, 베이스라인 모델로는 3층의 CNN 모델을 사용했다. 모델의 구조는 다음과 같다.

```cpp
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 102, 136, 32)      2432                                                                      
 conv2d_1 (Conv2D)           (None, 102, 136, 32)      25632                                                                    
 max_pooling2d (MaxPooling2D  (None, 51, 68, 32)       0         
 )                                                                                                                              
 dropout (Dropout)           (None, 51, 68, 32)        0                                                                       
 conv2d_2 (Conv2D)           (None, 51, 68, 64)        18496                                                                     
 conv2d_3 (Conv2D)           (None, 51, 68, 64)        36928                                                                    
 max_pooling2d_1 (MaxPooling  (None, 25, 34, 64)       0         
 2D)                                                                                                                            
 dropout_1 (Dropout)         (None, 25, 34, 64)        0                                                                         
 flatten (Flatten)           (None, 54400)             0                                                                        
 dense (Dense)               (None, 256)               13926656                                                                 
 dropout_2 (Dropout)         (None, 256)                0                                                                        
 dense_1 (Dense)             (None, 3)                  771                                                                       
=================================================================
Total params: 14,010,915
Trainable params: 14,010,915
Non-trainable params: 0
_________________________________________________________________
```
딥러닝 서버에서 모델을 학습시키고, TFLite 경량 모델로 변환하여 라즈베리파이에서 추론이 가능하도록 하였다. 이 모델로 중간 테스트 결과, 정확도가 충분치 않아 기구부 완성 이후 실제 환경에서 촬영한 사진을 사용하여 transfer learning을 추가로 진행하였다. 동일한 신발을 여러 번 반복 촬영하여 구두 33장, 슬리퍼 29장, 스니커즈 87장의 이미지를 얻었으며, train:test를 8:2 비율로 분할한 후에 이미지 회전 및 뒤집기를 통해 train data를 증강하였다. 기존 모델에서 flatten 층까지 83488개의 가중치를 동결시킨 이후에 0.0001의 학습률로 epoch 2000으로 하여 학습하였다. test accuracy는 96.8%로 높았지만 실제 신발 테스트 결과 정확도가 목표에 미치지 못했다.
 
  #### 신발 색상 구분
 ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/55d83961-0089-468f-adb8-4045221727ef)
  
  신발 색상 검출의 경우 <신발 개수 파악>에서 촬영한 이미지를 활용하고, 각 색상에 대한 mask를 생성하여 넓이를 비교하여 이 신발을 가장 잘 나타낼 수 있는 색상 하나를 선택한다. mask 생성 예시는그림 (a)와 같다. 신발장에 넣는 신발은 누구나 보기에도 한 가지 색상으로 명확히 드러나는 신발로 한정한다. RGB(빨간색, 초록색, 파란색)을 사용한 신발의 경우 회색, 검은색을 같이 사용하는 경우가 많기 때문에, 회색/검은색이 더 넓은 범위를 차지하더라도 RGB을 우선시하기로 하였다. RGB색 중 가장 많은 면적을 갖는 색을 선택하고, 만약 3가지 RGB색 모두 기준치에 미치지 못할 경우 회색/검은색 중 한 가지로 판별한다. 알고리즘은 그림 (b)와 같다. 인식을 쉽게 하기 위해 발판의 색을 흰색으로 제작한다.
 
 
------------------------------
## 아두이노 
 아두이노에서 사용되는 센서, 모터에 대한 설명 및 동작 시나리오에 대한 내용은 위에서 다루었다. 이 부분에서는 아두이노와 라즈베리파이와의 통신 부분을 주로 다루도록 하겠다.

- 아두이노 main loop (final.ino)
  

  <pre>
   <code>
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
   </code>
  </pre>

- 라즈베리파이 main loop (final.py)
  

<pre>
 <code>
  # 이 루프를 계속 반복하면서 입력, 출력 시나리오 실행 시 정지
while True:
    #ready to recieve data from Arduino
    print('ready to get data')
    
    # 출납 시나리오가 실행 중인 동안 입력 시나리오가 실행되지 않도록 함.
    while(firebase.remove == True):
        continue
    
    #아두이노에서 데이터 받음
    data_from_arduino=scenario.ser.readline().decode().strip()
    
    #Check insert_scenario
    if data_from_arduino=="Insert" :

        # 앱에서 버튼 눌러도 출납 시나리오가 실행되지 않도록 함
        firebase.doc_watch_request.unsubscribe()

        # 수납 시나리오 실행
        scenario.insert_scenario()

        # 수납 시나리오 실행 후 다시 출납 시나리오 실행될 수 있는 상태로 바꿈.
        firebase.doc_watch_request=firebase.doc_ref.on_snapshot(firebase.on_snapshot_request)

    time.sleep(0.5)
 </code>
</pre>
 
 아두이노와 라즈베리파이가 시리얼 통신을 이용하여 데이터를 주고 받는 과정은 다음과 같다. 사진 상에서 라즈베리파이 부분의 24번 라인( data_from_arduino=scenario.ser.readline().decode().strip())이 아두이노로부터 데이터가 올 때까지 대기하고 데이터가 오면 그 데이터 값을 리턴하는 명령어이다. 라즈베리파이의 main loop이 항상 돌아가야하기 때문에 아두이노 쪽에서는 별다른 이벤트(수납부 적외선 센서 인식)이 없다면 trivial한 데이터를 보내 라즈베리파이의 loop을 돌린다. 만약 수납부 적외선 센서가 인식되었을 시, 이때 아두이노는 trivial한 값이 아닌 수납시나리오의 시작을 알리는 데이터를 라즈베리파이로 보낸다. 이 값을 읽고 Rpi가 시나리오에 대한 동작하게 된다. 
 
 라즈베리파이 또한 아두이노로 데이터를 전송할 수 있어야 한다. 라즈베리파이 코드 위쪽에 정의된 send_data가 아두이노로 데이터를 전송하는 함수이다. send_data가 실행되었다면 아두이노 쪽에서는 249번 라인(if (Serial.available())과 같이 라즈베리파이가 보낸 데이터를 받아들일 수 있다. 


------------------------------
 ## 데이터 베이스
 
  Google Firebase를 이용해 신발장의 작동에 필요한 신발, 발판의 정보와 신발 이미지를 한번에 관리한다. Firestore Database의 경우 collection, document, field로 이루어져 있다.
  - init collection 
  
|document|field|설명|
|------|---|---|
|value|difference|shelf_location - shelf_num 값 저장하여 수납부, 출납부에 위치한 shelf_location 값 파악|

init 이름의 collection을 만들어 현재 shelf_num과 shelf_location 값의 차이를 저장한다.

 - shoe collection 

|field 이름|유형|설명|가능한 값|
|------|---|---|---|
|shoe_name|string|사용자가 지정한 신발의 이름	|-|
|shoe_type|string	|신발의 종류|shoes, slippers, sneakers|
|shoe_color|string	|신발의 색상|white, black,red, green, blue|
|shelf_num|number		|신발이 저장된 발판 번호|1, 2, 3, 4|
|shelf_location|number	|신발의 발판이 신발장의 어떤 위치에 해당하는지 사전 정의된 숫자|1, 2, 3, 4|
|shelf_status|boolean	|신발이 저장되어 있는지 유무	|True, False|
|order	|number	|어플리케이션 화면에 신발 정보를 띄울 순서	|1, 2, ... , 저장된 신발 개수|
|remain	|boolean|신발 정보를 삭제할지를 판단하기 위한 변수	|True, False|

신발 및 발판 정보를 저장할 collection의 이름은 shoes로 하고, document의 이름은 신발의 이미지 이름으로 한다. 이미지 이름은 촬영한 시점의 날짜-시간.jpg로 하여 유일하므로 document에 사용 가능하다. 각 document에 저장할 field의 정보는 위 표와 같다. 수납부의 shelf_location은 3, 출납부의 shelf_location은 1로 한다.


shelf_location의 갱신을 그림으로 나타내면 아래와 같다. 그림에서 회색 상자는 shelf_location을 의미하고, 빨강/노랑/초록/파랑 상자는 shelf_num을 의미한다. 초기에 발판이 모두 비어있는 경우에는 발판이 1칸(1번 발판이 3->2 위치로) 이동한다. shelf_location 2, 4 위치에 신발이 차 있는 경우에는 발판이 2칸(1번 발판이 3->1 위치로) 이동한다.

- 초기에 발판이 모두 비어있는 경우 shelf_location(회색 상자의 숫자)의 갱신
 ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/24670123-c5eb-4b05-b09e-85b110238ea0) 
 
 - shelf_location 2, 4 위치에 신발이 차 있는 경우 shelf_location의 갱신
 ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/8c59a1ea-6078-4e10-911f-4348ac102529)

shelf_location의 갱신을 그림으로 나타내면 위와 같다. 그림에서 회색 상자는 shelf_location을 의미하고, 빨강/노랑/초록/파랑 상자는 shelf_num을 의미한다. 초기에 발판이 모두 비어있는 경우에는 발판이 1칸(1번 발판이 3->2 위치로) 이동한다. shelf_location 2, 4 위치에 신발이 차 있는 경우에는 발판이 2칸(1번 발판이 3->1 위치로) 이동한다.


 - signal collection 

|document|field|설명|
|------|---|---|
|From_app_to_RPi|DocName|사용자가 출납을 원하는 신발의 이름을 RPi에게 전달하기 위해 사용|
|From_app_to_RPi|Fcm_token|FCM을 사용하기 위한 토큰|
|From_app_to_RPi|Request|출납 요청을 보낼 때 사용, 출납이 완료되기까지 앱의 동작을 막기 위함|
|Sign_question	|Sign_new|새로운 신발을 인식했을 때 RPi에서 사용자 응답을 기다리기 위해 사용|
|Sign_question	|which_shoe|기존 신발이 어떤 것인지를 RPi 가 알게끔 하는 용도|


'signal’ collection은 앱과 Rpi가 데이터를 주고 받기 위해서 사용된다. 해당 collection의 'from_app_to_RPi’ document에는 4가지 field가 있다. ‘request’ field는 앱에서 Rpi로 출납 요청을 보내기 위해 사용된다. 앱에서 출납 버튼을 누르면 해당 field 값이 ‘false’에서 ‘true’로 바뀌고 Rpi가 이를 읽어 출납 시나리오를 진행하는 방식이다. ‘DocName’ field는 사용자가 앱에서 선택한 신발(문서이름)을 저장하게 된다. Rpi는 해당 field를 읽어 사용자가 어떤 신발을 출납하려 하는지 알 수 있게 된다. ‘fcm_token’ field는 사용자 기기에 푸시알림인 FCM(Firebase Cloud Messaging)을 보내기 위해 사용된다. Rpi에서 앱으로 푸시알림을 보내기 위해서는 사용자 기기(스마트폰)에 생성되는 token 정보를 알아야 한다. 앱이 실행되면 ‘fcm_token’ field의 값을 생성된 token 값으로 변경하고 Rpi가 이를 읽고 앱으로 FCM을 보낼 수 있게 된다. 

‘signal’ collection에 ‘sign_question’ document에는 2가지 field가 있다. ‘sign_new’라는 field는 평소에는 ‘No’로 저장되어 있다가 FCM에 대한 사용자의 응답을 저장한다. FCM은 classification의 결과가 새로운 신발로 인식했을 때 보내지게 되는데 사용자는 이 신발이 정말 새로운 신발인지, 아니면 기존에 있던 신발인지를 선택하게 된다. 이에 대한 응답에 따라 ‘sign_new’에는 ‘yes’ 또는 ‘exist’이라는 값이 저장되게 된다. 만약 사용자가 기존 신발이라고 선택했을 경우, 신발 리스트에서 어떤 신발이었는지 다시 선택하게 되는데, 이 결과가 ‘which_shoe’ field에 저장되고 Rpi는 해당 field를 읽어 이에 대한 수납 처리를 진행할 수 있도록 한다.

 <img src="https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/1d020f92-1e57-4642-9621-2663e716da6d">
 
 Firestore Database에는 이미지를 업로드할 수 없기에, storage에 이미지를 저장하고 Firestore Database에는 이미지의 주소를 저장한다. 
 
 
 
 
 
 -----------------------------
 ## Application
 어플리케이션의 경우 Git 저장소 내의 'firebase' 폴더 내에서 코드를 작성하였다. 아래는 상황별 어플리케이션 구동 양상이다.
 
 ### 구현사항 
 
 - 파이어스토어와 스토리지에 접근하여 신발에 대한 데이터를 가져온다.
 
 * 해당 데이터를 바탕으로 RecycleView를 구성, 신발 정보를 순차적으로 나열하고, 신발 사진, 신발 이름, 신발 보관 상태를 표시한다.
  
 * 신발 출납 버튼을 구현하여 보관중인 신발을 출납할 수 있도록 한다.
 
 * 신발 수납시, 기존 신발을 넣을 때와 새로운 신발을 넣을 떄를 구분. 새로운 신발로 인식될 경우 사용자에게 등록 여부를 물음
  
 * 기존 신발을 새 신발로 인식했을 때의 오류 처리도 구현
 
 * 사용자 편의 증대를 위해 어플리케이션 내에서 신발 이름 수정, 목록 순서 변경, 신발 정보 삭제 등의 기능을 할 수 있도록 함. 
 
 
 
 
 ### Application scenario - 수납과정 
 ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/0bcf8177-08d7-4495-af86-afd385327913)

수납 과정에서 어플리케이션은 새로운 신발을 등록하고 classification의 잘못된 결과를 예방하기 위해 사용하게 된다. Rpi의 classification 결과가 기존 신발 리스트에 없는 종류일 경우, Rpi는 앱에게 푸시알림을 보내게 된다. 푸시 알림을 누르면 새롭게 인식된 신발의 사진과 두가지 선택사항이 있는 화면을 띄우게 된다. 버튼을 누르게 되면 Firestore 'signal’ collection에 'sign_question’ document의 'sign_new’ field 값을 바꾸게 된다. ＇네 등록할래요＇ 버튼을 누르게 되면 해당 field를 ‘yes’로 바꾸게 되고 Rpi가 이 field를 읽고 수납 시나리오를 진행하고 앱은 넣은 신발이 추가된 메인화면으로 돌아가게 된다. 만약 classification의 결과가 잘못되어 기존 신발을 새로운 신발로 인식할 경우, 사용자는 ‘기존신발이에요’ 버튼을 누르면 된다. 이 버튼을 누르면 사용자에게 이 신발이 어떤 신발이었는지 선택할 수 있는 화면으로 넘어가게 된다. 이 화면에 뜨는 신발은 보관상태가 ‘미보관＇인 신발들만 나타나게 된다. 사용자가 넣은 신발이 어떤 신발이었는지 선택하게 되면 Rpi는 그 신발에 대한 수납을 진행하고 앱은 선택한 신발의 상태가 ‘보관중’으로 바뀐 메인화면으로 돌아가게 된다.

 ### Application scenario - 출납 과정
 ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/4ef31cf8-bf13-415a-bbe5-61e98bc073d2)
 
 어플리케이션의 메인 화면은 firebase에 저장된 사용자의 신발 리스트 정보를 제공한다. 사용자가 정의한 신발의 이름, 신발 사진, 보관상태를 제공한다. 이를 통해 사용자는 신발장을 열어보지 않고도 어떤 신발이 보관되어 있는지 알 수 있다. 각 신발 인터페이스에는 '출납＇이라는 버튼이 있다. '미보관’ 상태의 신발의 ‘출납’ 버튼을 누르면 앱은 아무런 동작을 하지 않고 오직 토스트 메시지를 띄운다. 만약 ‘보관중’인 신발의 ‘출납’ 버튼을 누를 시, Rpi로 출납요청을 보내게 된다. ‘출납’ 버튼을 누를 시 firestore에 저장된 'signal’ collection에 'from_app_to_RPi’ document의 ‘request’ field를 true 상태로 바꾸게 되고 Rpi가 이를 인지하면 출납 시나리오가 시작된다. Filed를 바꾸고 앱은 로딩창을 띄우게 된다. 이는 출납이 완료될 때까지 앱의 행동을 막기 위함이다. 이후 Rpi가 신발의 정보를 수정하고 출납 동작을 마치게 되면 앱은 로딩창에서 메인화면으로 넘어가게 된다. 이 메인 화면에는 출납버튼을 누른 신발 상태 정보가 ‘미보관’으로 업데이트 되어 나타난다.

 
 ### Application scenario - 신발 정보 수정 
 ![image](https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/4b0528ed-beaa-41d1-b2e3-5e181757c461)
 
 어플리케이션을 사용하는 사용자의 편의를 증대시키기 위해서, 신발 목록을 편집할 수 있는 화면을 구현하였다. 어플의 메인화면 우측 하단에 있는 편집 버튼을 클릭하면, 신발 정보 수정 화면으로 넘어가게 된다. 수정 화면에서 할 수 있는 일은 신발 이름 변경, 신발 목록 순서 변경, 그리고 데이터 베이스에서 특정 신발 정보가 담겨져 있는 문서를 삭제하는 일이다. 위의 신발 분류 과정을 통해, 수납된 신발이 기존 신발과 매칭이 잘 된다면, 이러한 리스트 수정 과정은 사용자에게 큰 편의성을 가져다 줄 수 있다. 신발 순서 변경, 삭제 등의 기능은 드래그나 스와이프로 구현하는 것이 직관적이기 때문에, 드래그 앤 드랍을 할 시 리스트 순서 변경을, 그리고 왼쪽으로 밀면 신발 문서가 삭제되도록 하였다. 이는 Kotlin 내의 ItemTouchHelper이라는 클래스를 활용하여 구현할 수 있다. 혹시나 사용자가 순서 변경, 삭제 등의 기능에 대해서 알기 힘들 수 있으므로, 신발 리스트를 터치했을 때 안내 문구가 나오도록 하였다. 
 

 
 --------------
 
# Demonstration Video
## 수납 과정 - 새 신발 등록

https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/c13bd0f2-552b-4a32-bf9c-5cf81dd06f59

새로운 신발은 등록되어있지 않으므로, 새로운 신발이 감지되었으므로 등록할 것이냐는 메세지를 담은 FCM을 사용자에게 보낸다. 이후 사용자는 '등록할게요' 버튼을 눌러서 신발을 등록하고, 모터가 돌면서 정상적으로 수납과정을 수행하게 된다. 

## 수납 과정 - 기존 신발 수납

https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/e3c081ef-e1c6-46ea-8025-6ba264d77b82

이미 등록된 기존 신발을 수납할 경우, 별다른 메세지 없이 수납과정이 이루어지고, 보관상태가 변경된다. 

## 수납 과정 - 기존 신발을 새 신발로 인식했을 경우 

https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/b3ba6d81-61a5-4a3c-8219-4067f29252d0

기존 신발이더라도 새 신발로 인식이 될 경우 어플리케이션에 새 신발 등록 여부를 묻는 FCM이 오게 된다. 이후 사용자는 '기존 신발이에요' 버튼을 눌러서 해당 신발이 기존 신발 중 어떤 신발에 해당하는 지를 시스템으로 하여금 알 수 있도록 한다. 이후 데이터 개신 후 정상적으로 수납 과정이 이루어진다. 

## 수납 과정 - 신발이 정상적으로 들어가지 않았을 경우

https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/6bfb9aeb-d9b6-4f0d-a400-feb6c82dffc3

신발이 하나만 들어갔다거나 하는 정상적이지 않은 상황의 경우,  스피커를 통해 사용자에게 신발이 정상적으로 들어가지 않았음을 알린다. 이는 사용자가 신발 두 짝을 수납부에 정상적으로 넣을때까지 반복되며, 신발이 정상적으로 들어갔을 경우 스피커 알림을 멈추고 수납 과정을 수행한다. 

## 출납 과정

https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/15393270-29ea-435e-b47d-a056ea21b8c8

  어플리케이션 메인 화면의 출납 버튼을 누르면 해당 신발을 출납부에 위치하도록 모터 구동, 그리고 사용자가 신발을 꺼내는 것이 확인이 되면 빈 발판이 수납부에 위치하도록 하여, 이후 수납과정에서 문제가 생기지 않도록 한다.

## 어플리케이션 - 사용자 편의 기능 

https://github.com/ktwktw109/ESE2023_AutomaticStorageShoeRack/assets/108117940/d19de407-4630-4717-bd93-8a5f4796fc29

어플리케이션을 사용하는 사용자의 편의를 증대시키기 위해, 신발 이름 변경 및 리스트 순서 변경, 그리고 삭제 기능을 구현하였다. 리스트의 순서 변경 및 삭제 기능은 kotlin의 ItemTouchHelepr 클래스를 활용하여, 드래그 시  리스트 순서 변경, 스와이프 시 신발을 데이터 베이스에서 삭제 하도록 한다(더이상 수납장에 보관을 원치 않는 신발의 경우.)














 
 
 
