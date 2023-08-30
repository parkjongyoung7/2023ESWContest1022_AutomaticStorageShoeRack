#!/usr/bin/python
#
import sys
import random
import serial
import shutil
import os
sys.path.append('/home/ktw/Documents/emb/ESE2023_AutomaticStorageShoeRack/RPisrc')
import sendimage
import shoe_detect_nums
import time
import classification
import color_detection
#import firebase
#import scenario
from firebase_admin import credentials, firestore, storage, initialize_app
#from firebase import fcm_server_key, registration_id
from pyfcm import FCMNotification

#cred = credentials.Certificate("/home/ktw/Documents/emb/ESE2023_key.json") # 키 파일은 라즈베리파이에 저장되어 있음
#initialize_app(cred, {'storageBucket': f'emb-test-bdf82.appspot.com'}) # storage에서 gs:// 뒤의 내용 찾아서 적기
bucket = storage.bucket() # 버킷은 storage에서 데이터를 보관하는 기본 컨테이너
db = firestore.client()

def process_shoe(image_name, documentName):
    #moved_img = shutil.move('./'+image_name, '/home/ktw/shoes/'+image_name)

    # classification
    shoe_type = classification.shoeClassification(image_name)
    
    shoe_color = color_detection.main_color(image_name)
    
    '''
    # 테스트용 임의 지정
    shoe_color = str(random.randint(0, 99))
    shoe_type = str(random.randint(0, 99))
    shoe_color = 'blue'
    shoe_type = 'slippers'''
    
    print('shoe type is ', shoe_type)
    print('shoe color is ', shoe_color)

    # 이미지를 스토리지에 업로드 후 url을 shoe_image에 저장
    #shoe_image = sendimage.imageUploadtoStorage(image_name)

    #shelves = db.collection('shoes').stream()

    # 현재 수납부의 shelf_num 확인
    storage_shelf_num = firebase.get_receipt_shelf_num()

    # 이미지를 업로드하고 url을 image_url에 저장
    image_url = sendimage.imageUploadtoStorage(image_name, documentName)

    # 신발이 기존에 존재하는 신발인지 확인
    shoe_doc, shoe_id = firebase.get_existingshoe_doc(shoe_type, shoe_color)
    
    if shoe_doc is None:
        firebase.create_shoe_doc(documentName, shoe_type, shoe_color, storage_shelf_num)
        result=firebase.send_push_notification(fcm_server_key, registration_id, documentName + '.jpg')
        print(result)
        
        while db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'No':
            print("1")
            time.sleep(1)
            continue
        

        if db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'exist':
            while db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'exist':
                time.sleep(1)
                if db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'No':
                    break
            shoe_doc_name = db.collection('signal').document('sign_question').get().to_dict()['which_shoe']
            print(shoe_doc_name)
            print(type(shoe_doc_name))
            shoe_doc = db.collection('shoes').document(shoe_doc_name)
            shoe_doc.update({
                'shelf_num': storage_shelf_num,
                'shelf_status': True,
                'shelf_location': 3
            })
            documentName = shoe_doc_name
        print("2")
            # 사진 삭제 코드 추가
    


    # 기존 신발의 경우 
    else:
        shoe_doc.update({
            'shelf_num': storage_shelf_num,
            'shelf_status': True,
            'shelf_location': 3
        })
        documentName = shoe_id
        # 사진 삭제 코드 추가

    #firebase.button_pressed.clear()
    print("3")
    db.collection('signal').document('sign_question').update({'sign_new': 'No'})
    print("4")
    # 빈 발판을 empty_shelf_num에, 움직여야 하는 모터 회전각을 motor_angle에 저장
    empty_shelf_num, motor_angle = firebase.get_empty_shelf_location(storage_shelf_num)

    # 빈 발판이 존재하는 경우
    if empty_shelf_num is not None:
        
        doc = db.collection('shoes').document(documentName)
        doc.update({'shelf_status': True})

        firebase.rotate_shelf_locations(motor_angle)

        firebase.update_difference(motor_angle)

    return motor_angle


def insert_scenario():
    global documentName
    #Loop for take a picture and confrim picture.
    while True :
        time.sleep(4) #wait for aligning shoes
        #take picture code
        imageName = None
        while imageName is None:
            imageName, documentName=sendimage.execute_camera()
        print(imageName)
        #사진 판단해서 아두이노로 메세지를 보냄
        IsAligned=shoe_detect_nums.shoe_detect_nums(imageName)
        
        #1 센서가 오작동했다면
        if IsAligned=='no shoe\n' :
            print(' no shoe')
            scenario.send_data(IsAligned)
            #확인한 사진은 삭제
            os.remove(imageName)
            return
        
        
        #2 신발이 똑바르지 않다면
        if IsAligned=='sort please\n' :
            print(' sort please')
            scenario.send_data(IsAligned)
            #확인한 사진은 삭제
            os.remove(imageName)
            continue
            
        #3 사진이 괜찮다면 다음 loop를 돌리기 위해서 보낸다. 단계를 진행한다
        if IsAligned=='ok\n' :
            print(' ok')
            scenario.send_data(IsAligned)
            time.sleep(1) #아두이노가 먼저 메세지를 받는 상태에 가기를 희망
            break
    
    motor_angle = process_shoe(imageName, documentName)

    # 아두이노가 모터 움직일 준비됐는지 확인
    while True:
        data_from_arduino=scenario.ser.readline().decode().strip()
        if data_from_arduino=='Ready' :
            break

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    print('move motor')
    scenario.send_data(motor_angle)

    #RPi는 모터가 멈출 때까지 행동을 기다림
    
    print('moving motor, angle: ' + motor_angle)
    data_from_arduino=scenario.ser.readline().decode().strip()
    if data_from_arduino=='Done' :
        print('get Done')

    scenario.send_data('Done\n')

'''
def remove_scenario(image_name):
    #shelves = db.collection('shoes').stream()
    doc = db.collection('shoes').document(image_name)

    ### 나갈 신발을 출납 위치로
    remove_doc_location = db.collection('shoes').document(image_name).get().to_dict()['shelf_location']
    remove_motor_angle = (remove_doc_location - 1) * 90

    if remove_motor_angle > 180:
        remove_motor_angle -= 360

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    print('move motor')
    #scenario.send_data('move motor\n')

    firebase.rotate_shelf_locations(remove_motor_angle)
    firebase.update_difference(remove_motor_angle)

    ### 빈 발판을 수납 위치로

    # 발판 shelf_status False로 변경
    doc.update({'shelf_status': False})

    # 현재 수납부의 shelf_num 확인
    storage_shelf_num = firebase.get_receipt_shelf_num()
    print('storage_shelf_num is: ', storage_shelf_num)

    # 빈 발판을 empty_shelf_num에, 움직여야 하는 모터 회전각을 motor_angle에 저장
    empty_shelf_num, motor_angle = firebase.get_empty_shelf_location(storage_shelf_num)
    print('moving motor, angle: ' + motor_angle)

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    scenario.send_data(motor_angle)
    
    # 빈 발판이 존재하는 경우
    if empty_shelf_num is not None:
        firebase.rotate_shelf_locations(motor_angle)
        firebase.update_difference(motor_angle)
'''
#main 시작
#ser=scenario.ser

'''
while True:
    
    print('ready to get data')
    #ready to recieve data from Arduino
    
    while(firebase.remove == True):
        continue
    
    #아두이노에서 데이터 받을 때까지 대기함.
    data_from_arduino=scenario.ser.readline().decode().strip()
    
    # 출납 시나리오 실행 시 코드 멈춤
    #Check insert_scenario
    if data_from_arduino=="Insert" :
        firebase.doc_watch_request.unsubscribe()
        
        insert_scenario()
        firebase.doc_watch_request=firebase.doc_ref.on_snapshot(firebase.on_snapshot_request)

    time.sleep(0.5)
'''
    #insert_scenario()
#imageName, documentName=sendimage.execute_camera()

#IsAligned=shoe_detect_nums.shoe_detect_nums(imageName)

imageName = '/home/ktw/shoes/20230618-171255.jpg'
shoe_type = classification.shoeClassification(imageName)
    
shoe_color = color_detection.main_color(imageName)
    
print('shoe type is ', shoe_type)
print('shoe color is ', shoe_color)