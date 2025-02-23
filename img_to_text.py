# https://huggingface.co/stabilityai/stable-diffusion-2-depth

# https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/stable_diffusion/stable_diffusion_2.md?ysclid=m709apofgc89030639
# https://github.com/Dmukherjeetextiles/background-remover/blob/main/app.py


# https://dev.to/jeremycmorgan/how-to-generate-ai-images-with-stable-diffusion-xl-in-5-minutes-4ael?ysclid=m705xex0wu329090478
# https://requests.readthedocs.io/en/latest/user/quickstart/
# https://timeweb.cloud/tutorials/python/vvedenie-v-rabotu-s-bibliotekoj-requests-v-python?ysclid=m70gsl6zpl441410737
# https://stackoverflow.com/questions/17733133/loading-image-from-flasks-request-files-attribute-into-pil-image
# https://python-scripts.com/requests?ysclid=m70b2l58ex730107366



# pip install --upgrade pip
# pip install --upgrade diffusers[torch]
# pip install transformers Flask requests


from flask import Flask, request, jsonify, send_file
import os
import base64
from PIL import Image
from io import BytesIO
import ollama

app = Flask(__name__)

# Директория для сохранения загруженных изображений
UPLOAD_FOLDER = 'temp'  # Измените на желаемую директорию
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Создаем директорию, если она не существует



@app.route('/upload_image', methods=['POST'])
def upload_image():
    print(request);
    if request.method == 'POST':
        data = request.get_json()
        if 'image_data' not in data or 'image_name' not in data:
            return jsonify({'error': 'Отсутствуют данные изображения или имя изображения'}), 400
        
        image_data = data['image_data']
        image_name = data['image_name']
        content = data['content']
        print(image_data);

        # Декодируем данные изображения в base64
        try:
            image_bytes = base64.b64decode(image_data)
            image_path = os.path.join(UPLOAD_FOLDER, image_name)
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)

            print(f"Изображение сохранено по пути: {image_path}")

            # Создаем описание для выходного изображения
            response = ollama.chat(
                model='llama3.2-vision',
                messages=[{
                    'role': 'user',
                    'content': f'{content}',
                    'images': [image_path]  # Убедитесь, что путь правильный
                },],

            options={
                'temperature': 0.1, # значение от 0,0 до 0,9 (или 1) определяет уровень креативности модели или ее неожиданных ответов.
                # 'top_p': 0.9, #  от 0,1 до 0,9 определяет, какой набор токенов выбрать, исходя из их совокупной вероятности.
                # 'top_k': 90, # от 1 до 100 определяет, из скольких лексем (например, слов в предложении) модель должна выбрать, чтобы выдать ответ.
                # # 'num_ctx': 131000, # устанавливает максимальное используемое контекстное окно, которое является своего рода областью внимания модели.
                # 'num_ctx': 8190, # saiga (max) ~ 6100 words
                # 'num_predict': 100, # задает максимальное количество генерируемых токенов в ответах для рассмотрения (100 tokens ~ 75 words).
            },
            )

            # Проверяем, есть ли ответ от модели
            if 'message' not in response or 'content' not in response['message']:
                return jsonify({'error': 'Не удалось получить ответ от модели'}), 400
            
            # Генерируем изображение с помощью модели диффузии
            prompt = response['message']['content'] #+ " do'nt draw text"
            print(f"Полученный запрос: {prompt}")
            os.remove(f'temp/{image_name}')

            return jsonify({'status': 'success', 'result': prompt}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Возвращаем сообщение об ошибке



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
  # Запускаем сервер на всех интерфейсах

