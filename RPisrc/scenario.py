import sys
import serial
import random
import os
import time
sys.path.append('/home/ktw/Documents/emb/ESE2023_AutomaticStorageShoeRack/RPisrc')
import sendimage
import shoe_detect_nums
import classification
import color_detection
import firebase
#from firebase_admin import credentials, firestore
#from firebase import fcm_server_key, registration_id
db = firebase.firestore.client()

ser=serial.Serial('/dev/ttyUSB0',9600)

def send_data(data_to_arduino):
    ser.write(data_to_arduino.encode())

def remove_motor_angle_to_str(angle):
    if angle == 90:
        return 'CCW1\n'
    elif angle == 180:
        return 'CCW2\n'
    elif angle == -90:
        return 'CW1\n'
    else:
        return 'stay\n'

def empty_shelf_to_insert(doc):
    # 발판 shelf_status False로 변경
    doc.update({'shelf_status': False})

    # 현재 수납부의 shelf_num 확인
    storage_shelf_num = firebase.get_receipt_shelf_num()
    print('storage_shelf_num is: ', storage_shelf_num)

    # 빈 발판을 empty_shelf_num에, 움직여야 하는 모터 회전각을 motor_angle에 저장
    empty_shelf_num, motor_angle = firebase.get_empty_shelf_location(storage_shelf_num)
    print('moving motor, angle: ' + motor_angle)

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    send_data(motor_angle)
    
    # 
    while True:
        data_from_arduino=ser.readline().decode().strip()
        print('data from arduino', data_from_arduino)
        if data_from_arduino=='Done' :
            #send_data('Done\n')
            break

    # 빈 발판이 존재하는 경우
    if empty_shelf_num is not None:
        firebase.rotate_shelf_locations(motor_angle)
        firebase.update_difference(motor_angle)
        
    db.collection('signal').document('from_app_to_RPi').update({'request': False})

    send_data('DatabaseDone\n')

def remove_scenario(image_name):
    send_data('remove_scenario\n')
    #shelves = db.collection('shoes').stream()
    doc = db.collection('shoes').document(image_name)

    ### 나갈 신발을 출납 위치로
    remove_doc_location = db.collection('shoes').document(image_name).get().to_dict()['shelf_location']

    # 모터 회전각 계산
    remove_motor_angle = (remove_doc_location - 1) * 90
    if remove_motor_angle > 180:
        remove_motor_angle -= 360
    print(remove_motor_angle)

    # 모터 회전각을 문자열로 변환
    remove_motor_angle = remove_motor_angle_to_str(remove_motor_angle)

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    print('move motor')
    print(remove_motor_angle)
    send_data(remove_motor_angle)
    
    while True:
        data_from_arduino=ser.readline().decode().strip()
        if data_from_arduino=='Done' :
            print('Done his')
            #send_data('Done\n')
            break

    firebase.rotate_shelf_locations(remove_motor_angle)
    firebase.update_difference(remove_motor_angle)

    send_data('DatabaseDone\n')

    ### 빈 발판을 수납 위치로
    while True:
        print('ready to get data')
        data_from_arduino=ser.readline().decode().strip()
        print('data from arduino', data_from_arduino)
        # 아두이노에서 신호 받기
        if data_from_arduino=='FindEmpty':
            empty_shelf_to_insert(doc)
            break

def newShoes(documentName, shoe_type, shoe_color, storage_shelf_num):
    # 새 신발에 대한 문서 생성
    firebase.create_shoe_doc(documentName, shoe_type, shoe_color, storage_shelf_num)

    # 앱으로 FCM을 보내고 결과 출력
    result=firebase.send_push_notification(firebase.fcm_server_key, firebase.registration_id, documentName + '.jpg')
    print(result)
    
    # 사용자가 FCM을 확인 후 앱에서 버튼을 누르기 전까지 멈춤
    while db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'No':
        print("processing FCM")
        time.sleep(1)
        continue
    
    # 사용자가 기존 신발이라고 선택한 경우
    if db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'exist':
        # 사용자가 목록에서 신발을 선택할 때까지 멈춤
        while db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'exist':
            time.sleep(1)
            if db.collection('signal').document('sign_question').get().to_dict()['sign_new'] == 'select':
                time.sleep(2)
                break
                
        time.sleep(2)
        # 사용자가 선택한 신발에 해당하는 문서 필드 업데이트
        shoe_doc_name = db.collection('signal').document('sign_question').get().to_dict()['which_shoe']
        shoe_doc = db.collection('shoes').document(shoe_doc_name)
        shoe_doc.update({
            'shelf_num': storage_shelf_num,
            'shelf_status': True,
            'shelf_location': 3
        })
        documentName = shoe_doc_name
    
    return documentName

def process_shoe(image_name, documentName):

    # 신발 종류 파악
    shoe_type = classification.shoeClassification(image_name)
    # 신발 색상 파악
    shoe_color = color_detection.main_color(image_name)
    
    print('shoe type is ', shoe_type)
    print('shoe color is ', shoe_color)

    # 현재 수납부의 shelf_num 확인
    storage_shelf_num = firebase.get_receipt_shelf_num()

    # 이미지를 업로드
    image_url = sendimage.imageUploadtoStorage(image_name, documentName)

    # 신발이 기존에 존재하는 신발인지 확인
    shoe_doc, shoe_id = firebase.get_existingshoe_doc(shoe_type, shoe_color)
    
    # 1. 넣은 신발이 새 신발이라고 판단한 경우
    if shoe_doc is None:
        documentName = newShoes(documentName, shoe_type, shoe_color, storage_shelf_num)

    # 2. 넣은 신발을 기존 신발이라고 판단했지만 실제로는 새 신발인 경우
    elif shoe_doc.get().to_dict()['shelf_status'] == True:
        shoe_type = 'unknown' + str(random.randint(0, 999))
        shoe_color = str(random.randint(0, 999))
        # 랜덤 숫자로 색상과 종류를 지정함
        documentName = newShoes(documentName, shoe_type, shoe_color, storage_shelf_num)

    # 3. 2. 넣은 신발을 기존 신발이라고 판단했고 실제로 데이터베이스에 존재하는 경우
    else:
        shoe_doc.update({
            'shelf_num': storage_shelf_num,
            'shelf_status': True,
            'shelf_location': 3
        })
        documentName = shoe_id
        
    # sign_new 필드를 초기 상태로 되돌림
    db.collection('signal').document('sign_question').update({'sign_new': 'No'})
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
            send_data(IsAligned)
            #확인한 사진은 삭제
            os.remove(imageName)
            return
        
        
        #2 신발이 똑바르지 않다면
        if IsAligned=='sort please\n' :
            print(' sort please')
            send_data(IsAligned)
            #확인한 사진은 삭제
            os.remove(imageName)
            continue
            
        #3 사진이 괜찮다면 다음 loop를 돌리기 위해서 보낸다. 단계를 진행한다
        if IsAligned=='ok\n' :
            print(' ok')
            send_data(IsAligned)
            time.sleep(1) #아두이노가 먼저 메세지를 받는 상태에 가기를 희망
            break
    
    motor_angle = process_shoe(imageName, documentName)

    # 아두이노가 모터 움직일 준비됐는지 확인
    while True:
        data_from_arduino=ser.readline().decode().strip()
        if data_from_arduino=='Ready' :
            break

    #아두이노에게 모터를 움직이라고 메세지를 보냄
    print('move motor')
    send_data(motor_angle)

    #RPi는 모터가 멈출 때까지 행동을 기다림
    print('moving motor, angle: ' + motor_angle)
    data_from_arduino=ser.readline().decode().strip()
    if data_from_arduino=='Done' :
        print('get Done')

    send_data('Done\n')