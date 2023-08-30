#!/usr/bin/python
import sys
sys.path.append('/home/ktw/Documents/emb/ESE2023_AutomaticStorageShoeRack/RPisrc')
import time
import firebase
import scenario
from firebase_admin import firestore, storage, initialize_app
from pyfcm import FCMNotification

bucket = storage.bucket() # 버킷은 storage에서 데이터를 보관하는 기본 컨테이너
db = firestore.client()

# 이 루프를 계속 반복하면서 수납, 출납 시나리오 실행 시 정지
while True:
    #ready to recieve data from Arduino
    print('ready to get data')
    
    #출납 시나리오가 실행 중인 동안 수납 시나리오가 실행되지 않도록 함.
    while(firebase.remove == True):
        continue
    
    # 아두이노에서 데이터 받음
    data_from_arduino=scenario.ser.readline().decode().strip()
    
    #Check insert_scenario
    # 아두이노에 연결된 적외선 센서에 물체가 감지되면, Insert 메시지를 수신하여 수납 시나리오 실행됨.
    if data_from_arduino=="Insert" :

        # 앱에서 버튼 눌러도 출납 시나리오가 실행되지 않도록 함
        firebase.doc_watch_request.unsubscribe()

        # 수납 시나리오 실행
        scenario.insert_scenario()

        # 수납 시나리오 실행 후 다시 출납 시나리오 실행될 수 있는 상태로 바꿈.
        firebase.doc_watch_request=firebase.doc_ref.on_snapshot(firebase.on_snapshot_request)

    time.sleep(0.5)