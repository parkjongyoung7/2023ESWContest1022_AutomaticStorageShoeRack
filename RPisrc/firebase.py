import sys
sys.path.append('/home/ktw/Documents/emb/ESE2023_AutomaticStorageShoeRack/RPisrc')
from firebase_admin import credentials, firestore, initialize_app, storage
from pyfcm import FCMNotification
import scenario
from threading import Event

# Create an event
button_pressed = Event()

bucket = storage.bucket() # 버킷은 storage에서 데이터를 보관하는 기본 컨테이너
db = firestore.client()

# 출납 시나리오가 실행되는지 확인하기 위해 생성한 변수
remove = False

# 발판 번호에 해당하는 정보 가져옴
def get_shelf_info(image_name):
    return db.collection('shoes').document(image_name).get().to_dict()

# 신발 종류와 색상에 맞는 document 리턴, 없으면 None 리턴
def get_existingshoe_doc(shoe_type, shoe_color):
    shoes = db.collection('shoes').where(u'shoe_type', u'==', shoe_type).where(u'shoe_color', u'==', shoe_color).stream()

    for shoe in shoes:
        return db.collection('shoes').document(shoe.id), shoe.id
    
    return None, None

# 새로운 신발이 들어올 경우 order field 값을 증가시키는 함수
def increment_order_field():
    # collection에서 모든 document를 가져옴
    docs = db.collection('shoes').get()
    for doc in docs:
        # 현재 order 필드의 값을 가져옴
        current_order = doc.to_dict().get('order', 0)

        # order 값 증가 후 값 업데이트
        new_order = current_order + 1
        doc.reference.update({'order': new_order})


# 새로운 신발이 들어올 경우 새 document 생성
def create_shoe_doc(image_name, shoe_type, shoe_color, storage_shelf_num):
    increment_order_field()
    doc_data = {
        'shoe_name': shoe_type + '_' + shoe_color,
        'shoe_type': shoe_type,
        'shoe_color': shoe_color,
        'shelf_status': True,
        'shelf_num': storage_shelf_num,
        'shelf_location': 3,
        'order': 0,
        'remain': True
    }
    db.collection('shoes').document(image_name).set(doc_data)

# 가장 가까운 빈 발판의 발판 번호와 모터 회전각 리턴
def get_empty_shelf_location(storage_shelf_num):
    global remove
    all_shelf_nums = [1, 2, 3, 4]
    print("storage_shelf_num is: ", storage_shelf_num)

    # 수납부의 발판 번호에 따른 가까운 발판 번호 탐색 순서
    nearest_shelf_nums = {1: [1, 2, 4, 3], 2: [2, 3, 1, 4], 3: [3, 4, 2, 1], 4: [4, 1, 3, 2]}
    nearest_empty_shelf_num = None

    # 차 있는 발판 번호와 비어 있는 발판 번호 확인
    occupied_shelf_nums = [doc.to_dict()['shelf_num'] for doc in db.collection('shoes').get() if doc.to_dict()['shelf_status'] == True]
    empty_shelf_nums = list(set(all_shelf_nums) - set(occupied_shelf_nums))
    print("occupied_shelf_nums are: ", occupied_shelf_nums)
    print("empty_shelf_nums are: ", empty_shelf_nums)

    # 딕셔너리를 순회하면서 해당 발판 번호에 해당하는 발판이 비어있는지 확인
    for shelf_num in nearest_shelf_nums[storage_shelf_num]:
        #print("shelf num is", shelf_num, empty_shelf_nums)
        # 비어있는 발판이 있는 경우 번호를 저장 후 루프 빠져나감
        if shelf_num in empty_shelf_nums:
            nearest_empty_shelf_num = shelf_num
            break

    # 비어있는 발판이 없는 경우 모터는 움직이지 않음, 바로 리턴
    if nearest_empty_shelf_num is None or nearest_empty_shelf_num == storage_shelf_num:
        return None, 'stay\n'
    print(nearest_empty_shelf_num, storage_shelf_num)

    # 각 경우마다 모터 회전각 다르게 리턴
    if nearest_empty_shelf_num - storage_shelf_num == 1 or (nearest_empty_shelf_num == 1 and storage_shelf_num == 4):
        return nearest_empty_shelf_num, 'CCW1\n'
    elif nearest_empty_shelf_num - storage_shelf_num == -1 or (nearest_empty_shelf_num == 4 and storage_shelf_num == 1):
        return nearest_empty_shelf_num, 'CW1\n'
    else:
        return nearest_empty_shelf_num, 'CCW2\n'
    
# 지정한 문서의 shelf_location을 지정한 값으로 업데이트
def update_shelf_info(doc, shelf_location):
    if shelf_location is not None:
        doc.update({
            'shelf_location': shelf_location
        })

# 모터 회전각에 따라 shelf_location 값 업데이트
def rotate_shelf_locations(motor_angle):
    shelves = db.collection('shoes').stream()
    for doc in shelves:
        # 보관중인 신발만 업데이트
        if doc.to_dict()['shelf_status'] == True:
            shelf_loc = doc.to_dict()['shelf_location']
            print('first', shelf_loc)
            print('motor angle', motor_angle)
            if motor_angle == 'CCW1\n':
                shelf_loc = shelf_loc - 1 if shelf_loc > 1 else 4
            elif motor_angle == 'CW1\n':
                shelf_loc = shelf_loc + 1 if shelf_loc < 4 else 1
            elif motor_angle == 'CCW2\n':
                shelf_loc = shelf_loc - 2 if shelf_loc > 2 else shelf_loc + 2
            print('second', shelf_loc)
            update_shelf_info(db.collection('shoes').document(doc.id), shelf_loc)

# 모터 회전각에 따라 shelf_location - shelf_num 값인 difference 값 업데이트
def update_difference(motor_angle):
    difference = db.collection('init').document('value').get().to_dict()['difference']
    if motor_angle == 'CCW2\n':
        difference -= 2
    elif motor_angle == 'CCW1\n':
        difference -= 1
    elif motor_angle == 'CW1\n':
        difference += 1

    if difference < -1:
        difference += 4
    if difference > 2:
        difference -= 4
    db.collection('init').document('value').update({'difference': difference})
    print("updated difference", difference)

# 수납부 발판 번호 확인
def get_receipt_shelf_num():
    difference = db.collection('init').document('value').get().to_dict()['difference']
        
    return 3 - difference

# 출납부 발판 번호 확인
def get_remove_shelf_num():
    difference = db.collection('init').document('value').get().to_dict()['difference']
    shelf_num = 1 - difference
    if shelf_num < 1:
        shelf_num += 4
    return shelf_num

#FCM을 앱으로 보내는 함수 - new_picture_name 새로 찍은 사진 name 전달하기 (새 신발로 인식했을 때 사용)
def send_push_notification(fcm_server_key, registration_id, new_picture_name):

    fcm_client = FCMNotification(api_key=fcm_server_key)
    message={
        "key1":new_picture_name
    }
   
    print(message)
    result = fcm_client.notify_single_device(registration_id=registration_id, data_message=message)
    print(result)

#request 값이 true로 변경되었을 때 이벤트 처리 콜백함수 등록
def on_snapshot_request(doc_snapshot, changes, read_time):
    global remove
    remove = True
    for doc in doc_snapshot:
        if doc.exists:
            data=doc.to_dict()
            if 'request' in data and data['request']==True:
                print("Request received!")
                #여기에 원하는 기능 설정!-출납시나리오 시작하도록
                image_name = doc.get("DocName")
                scenario.remove_scenario(image_name)
        else:            print("Document does not exist")
    remove = False

#fcm_token 값이 변경되었을 때 이벤트 처리 콜백함수 등록
def on_snapshot_token(doc_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'MODIFIED':
            data = doc_snapshot[change.document.id].to_dict()
            if 'fcm_token' in data:
                current_value = data['fcm_token']
                previous_value = change.document.get('fcm_token').previous_value
                if previous_value != current_value:
                    print("Token has changed:", current_value)
                    # 바뀐 정보 저장
                    global registration_id
                    registration_id = current_value

#App으로부터 신호를 받기 위한 과정
#FIRESOTRE의 signal 컬렉션 참조
signal_ref=db.collection('signal')
#'from_app_to_RPi' 문서 참조
doc_ref=signal_ref.document('from_app_to_RPi')
#sign_qusetion 문서 참조
doc_sign=signal_ref.document('sign_question')

#실시간 변경 감지 리스너 등록 - 이를 통해 main loop 에서 계속 request를 참조할 필요없음->읽기용량 절약
doc_watch_request=doc_ref.on_snapshot(on_snapshot_request)
#실시간 변경 감지 리스너 등록 - 이를 통해 사용자가 앱에서 토큰이 바뀌어도 다시 등록하여 fcm이 가능하도록 함
doc_watch_token=doc_ref.on_snapshot(on_snapshot_token)

# FCM 서버 키 설정 -firebase-fcm-key 정보 보면 된다
global fcm_server_key
global registration_id
global new_picture_name
fcm_server_key = 'AAAAhpKhpAk:APA91bF2PHbSuJT1BkBX9vI8XrUZnYvnfdZw9P9dwxDItlNux9oSI6D1KFQU6p5Uj0ct26Bhyl60hRGW0CBBwx3jOEnJv8J_d5kPHBJ7YX3Xyz5Lk8t3k1oX9GpqKW6xIozNNVafTFcb'
registration_id = doc_ref.get().get('fcm_token')
new_picture_name="hihihi.jpg" #실제로는 찍은 이미지 사진 name이 들어가야함
