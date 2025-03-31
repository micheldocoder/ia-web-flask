from flask import Flask, request, render_template
import os
import uuid
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    imagem = request.files.get('imagem')
    acao = request.form.get('acao')

    if not imagem or not acao:
        return "Erro: imagem ou ação não fornecida", 400

    nome_imagem = str(uuid.uuid4()) + "_" + imagem.filename
    caminho_imagem = os.path.join(UPLOAD_FOLDER, nome_imagem)
    imagem.save(caminho_imagem)

    caminho_video_base = f'controle/{acao}.mp4'
    url_api = "https://xyz.ngrok.io/processar"  # Substitua pelo seu endpoint do Colab

    with open(caminho_imagem, 'rb') as img_file, open(caminho_video_base, 'rb') as vid_file:
        files = {
            'imagem': img_file,
            'video_base': vid_file
        }
        resposta = requests.post(url_api, files=files)

    if resposta.status_code == 200:
        nome_saida = str(uuid.uuid4()) + "_saida.mp4"
        caminho_saida = os.path.join(OUTPUT_FOLDER, nome_saida)
        with open(caminho_saida, 'wb') as f:
            f.write(resposta.content)
        return render_template('resultado.html', video_path=caminho_saida)
    else:
        return f"Erro ao gerar vídeo: {resposta.status_code}", 500

if __name__ == '__main__':
    app.run()
