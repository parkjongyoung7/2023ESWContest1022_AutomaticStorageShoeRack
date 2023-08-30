#!/usr/bin/python
#
import sys
import serial
import os
sys.path.append('/home/dan/Desktop/ESEPRO/ESE2023_AutomaticStorageShoeRack')
import sendimage
import shoe_detect_nums
import time
import classification
import color_detection
import firebase
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("/home/ktw/Documents/emb/ESE2023_key.json") # 키 파일은 라즈베리파이에 저장되어 있음
initialize_app(cred, {'storageBucket': f'emb-test-bdf82.appspot.com'}) # storage에서 gs:// 뒤의 내용 찾아서 적기
bucket = storage.bucket() # 버킷은 storage에서 데이터를 보관하는 기본 컨테이너
db = firestore.client()


def process_shoe(image_name):
    moved_img = shutil.move('./'+image_name, '/home/ktw/'+image_name)
    
    # classification
    shoe_type = classification.shoeClassification(moved_img)
    print('shoe type is ', shoe_type)
    shoe_color = color_detection.main_color(moved_img)
    print('shoe color is ', shoe_color)

    shelves = db.collection('shoes').stream()

    # 현재 수납부의 shelf_num 확인
    storage_shelf_num = [doc.to_dict()['shelf_num'] for doc in shelves if doc.to_dict()['shelf_location'] == 3][0]

    # 이미지를 업로드하고 url을 image_url에 저장
    image_url = sendimage.imageUploadtoStorage(image_name)

    # 신발이 기존에 존재하는 신발인지 확인
    shoe_doc = firebase.get_existingshoe_doc(shoe_type, shoe_color)

    if shoe_doc is None:
        # 새 신발의 경우 새 document 생성
        firebase.create_shoe_doc(image_name, shoe_type, shoe_color, storage_shelf_num)
    # 기존 신발의 경우 
    else:
        shoe_doc.update({
            'shelf_num': storage_shelf_num,
            'shelf_status': True,
            'shelf_location': 3
        })

    # 빈 발판을 empty_shelf_num에, 움직여야 하는 모터 회전각을 motor_angle에 저장
    empty_shelf_num, motor_angle = firebase.get_empty_shelf_location(storage_shelf_num)

    
    doc = db.collection('shoes').document(image_name)
    doc.update({'shelf_status': True})

    # 빈 발판이 존재하는 경우
    if empty_shelf_num is not None:
        firebase.rotate_shelf_locations(shelves, motor_angle)
        firebase.update_shelf_locations(doc)

    return motor_angle

def send_data(data_to_arduino) :
    ser.write(data_to_arduino.encode())

def insert_scenario():
    #Loop for take a picture and confrim picture.
    while True :
        time.sleep(2) #wait for aligning shoes
        #take picture code
        imageName=sendimage.execute_camera()
        print(imageName)
        #사진 판단해서 아두이노로 메세지를 보냄
        IsAligned=shoe_detect_nums.shoe_detect_nums(imageName)
        #확인한 사진은 삭제
        os.remove(imageName)
        #1 센서가 오작동했다면
        if IsAligned=='no shoe\n' :
            print(' no shoe')
            send_data(IsAligned)
            return 
        
        
        #2 신발이 똑바르지 않다면
        if IsAligned=='sort please\n' :
            print(' sort please')
            send_data(IsAligned)
            continue
            
        #3 사진이 괜찮다면 다음 loop를 돌리기 위해서 보낸다. 단계를 진행한다
        if IsAligned=='ok\n' :
            print(' ok')
            send_data(IsAligned)
            time.sleep(1) #아두이노가 먼저 메세지를 받는 상태에 가기를 희망
            break
    
    process_shoe(imageName)

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    send_data('move motor\n')

    #RPi는 모터가 멈출 때까지 행동을 기다림
    while True :
        data_from_arduino=ser.readline().decode().strip()
        if data_from_arduino=='Done' :
            # shelf_location 정보 업데이트


            print('get Done')
            break
    

    send_data('Done\n')

def remove_scenario(image_name):
    shelves = db.collection('shoes').stream()
    doc = db.collection('shoes').document(image_name)

    ### 나갈 신발을 출납 위치로
    remove_doc_location = db.collection('shoes').document(image_name).get().to_dict()['shelf_location']
    remove_motor_angle = (remove_doc_location - 1) * 90

    if remove_motor_angle > 180:
        remove_motor_angle -= 360

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    print('move motor')
    #send_data('move motor\n')

    firebase.rotate_shelf_locations(remove_motor_angle)
    firebase.update_shelf_locations(doc)

    ### 빈 발판을 수납 위치로
    # 현재 수납부의 shelf_num 확인
    storage_shelf_num = [doc.to_dict()['shelf_num'] for doc in shelves if doc.to_dict()['shelf_location'] == 3][0]

    # 빈 발판을 empty_shelf_num에, 움직여야 하는 모터 회전각을 motor_angle에 저장
    empty_shelf_num, motor_angle = firebase.get_empty_shelf_location(storage_shelf_num)

    # 빈 발판이 존재하는 경우
    if empty_shelf_num is not None:
        firebase.rotate_shelf_locations(shelves, motor_angle)
        firebase.update_shelf_locations(doc)

#main 시작
ser=serial.Serial('/dev/ttyUSB0',9600)


while True:
    print('ready to get data')
    #ready to recieve data from Arduino
    #아두이노에서 데이터 받을 때까지 대기함.
    data_from_arduino=ser.readline().decode().strip()
    
    #Check insert_scenario
    if data_from_arduino=="Insert" :
        insert_scenario()
    time.sleep(0.5)
        
    