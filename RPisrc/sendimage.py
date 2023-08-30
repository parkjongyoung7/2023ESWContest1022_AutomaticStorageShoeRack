from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import cv2
from uuid import uuid4

#cred = credentials.Certificate("/home/ktw/Documents/emb/ESE2023_key.json") # 키 파일은 라즈베리파이에 저장되어 있음
cred = credentials.Certificate("/home/ktw/Downloads/AndroidTest.json") # 키 파일은 라즈베리파이에 저장되어 있음
#firebase_admin.initialize_app(cred, {'storageBucket': f'emb-test-bdf82.appspot.com'}) # storage에서 gs:// 뒤의 내용 찾아서 적기
firebase_admin.initialize_app(cred, {'storageBucket': f'androidtest-34c93.appspot.com'})
bucket = storage.bucket() # 버킷은 storage에서 데이터를 보관하는 기본 컨테이너

def imageUploadtoStorage(imageName, documentName): # image를 firebase storage에 업로드
    blob = bucket.blob('shoeImages/'+documentName + '.jpg') # blob 객체 생성
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} # access token 필요
    blob.metadata = metadata

    # 파일 업로드
    blob.upload_from_filename(filename = imageName, content_type='image/jpeg')
    return blob.public_url

def execute_camera(): # 사진 촬영
    # 현재 날자와 시간을 이미지의 이름으로 함
    now = datetime.now()
    imageName = '/home/ktw/shoes/'+now.strftime("%Y%m%d-%H%M%S") + '.jpg'
    documentName = now.strftime("%Y%m%d-%H%M%S")
    # 카메라를 통해 사진 1장 촬영
    capturedImage = cv2.VideoCapture(0) #ls /dev/video*로 확인하기
    ret, frame = capturedImage.read() 
    if not ret: # 사진 촬영 실패시
        print("Failed to capture image")
        capturedImage.release()
        return None, None
    cv2.imwrite(imageName, frame)
    capturedImage.release() # 사진 1장만 촬영하므로 videocapture release
    print(imageName+'pictured')
    
    # firebase에 업로드
    #imageUploadtoStorage(imageName, documentName) #<- 이 코드는 main에 넣어야 할
    
    return imageName, documentName

#execute_camera()

