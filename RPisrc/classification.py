import numpy as np
import cv2
import os
from os import walk
from tqdm import tqdm
from skimage.transform import resize 

import tflite_runtime.interpreter as tflite

shoe_items = {0:'shoes', 1:'slippers', 2:'sneakers'}

def shoeClassification(shoe_image):
  # tflite interpreter 설정
  interpreter = tflite.Interpreter(model_path= '/home/ktw/Documents/emb/ESE2023_AutomaticStorageShoeRack/RPisrc/shoe_model.tflite', num_threads=2)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

### Try predicting label with one validation sample (inference)
  # 이미지 크기 모델 입력에 맞도록 조정, interpolation 옵션 조정 가능
  shoe_image = cv2.imread(shoe_image)
  shoe_image = cv2.resize(shoe_image, dsize=(136,102), interpolation=cv2.INTER_LINEAR)
  img_array = np.asarray(shoe_image) # numpy 형태로 변환

  # 추론 실행
  x = np.expand_dims(img_array.astype('float32'), 0)
  try:
    interpreter.set_tensor(input_details[0]['index'], x)
  except:
    print("error!!")
  interpreter.invoke()
  output_data = interpreter.get_tensor(output_details[0]['index'])
  results = np.squeeze(output_data)

  # 결과 반환
  classification_result = shoe_items[np.argmax(results)]
  return classification_result # shoes/slippers/sneakers 중 하나 반환(문자열)
