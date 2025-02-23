# pip install requests

# source NEUROCHAGEIMAGES/bin/activate

import requests
import os
import base64

# Определяем адрес сервера
server = 'http://192.168.100.149:6000'  # Измените на IP-адрес вашего сервера

# Указываем имя файла изображения и полный путь
old_name = '5.png'

# Проверяем, существует ли указанный файл изображения
if os.path.isfile(old_name):
    print(f"Файл {old_name} найден.")
else:
    print(f"Файл {old_name} не найден.")
    exit(1)  # Выход, если файл не найден

# Читаем файл изображения и кодируем его в base64
with open(old_name, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# Отправляем данные изображения на сервер
response = requests.post(f"{server}/upload_image", json={
    "image_data": encoded_string, 
    "image_name": os.path.basename(old_name),
    "content": "Что на картинке?" #"Какой электроный разъем изображен на картинке"
    })

print(response.text)

'''
{"result":"The image shows a photograph of Donald Trump. 
He appears to be wearing a blue suit jacket, white shirt and red tie. 
There are some indistinct white shapes behind him that may be signs or text. 
The background is dark blue with some bright spots of light which may indicate 
stage lights.","status":"success"}
'''