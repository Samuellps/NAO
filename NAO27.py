# -*- coding: utf-8 -*-
from naoqi import ALProxy
import os
import time
import socket
import json
import codecs

# Criar um socket cliente
def nao_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 🔹 Aguarda até 10 segundos pelo servidor
    server_ready = False
    for _ in range(20):  # Tenta conectar por até 10 segundos
        try:
            client_socket.connect(('127.0.0.1', 6005))  # Conecta ao servidor Python 3
            server_ready = True
            break
        except socket.error:
            print("Aguardando servidor Python 3...")
            time.sleep(0.5)

    if not server_ready:
        print("Erro: Não foi possível conectar ao servidor Python 3!")
        return None

    var_ativacao = "ok"  # Variável de ativação
    client_socket.send(var_ativacao.encode())  # Ativa o Python 3
    response = client_socket.recv(1024).decode('utf-8')  # Retorna a resposta do Python 3

    client_socket.close()
    return response

# Conectar ao NAO
ip = "192.168.59.225"
port = 9559
vol_NAO = 60
# Criação de Proxy para os módulos
audio_recorder = ALProxy("ALAudioRecorder", ip, port)
face_detection = ALProxy("ALFaceDetection", ip, port)
memoryProxy = ALProxy("ALMemory", ip, port)
tts = ALProxy("ALTextToSpeech", ip, port)
audio_proxy = ALProxy("ALAudioDevice", ip, port)

# Configurar o local onde o arquivo de áudio será salvo no robô
audio_file = "/home/nao/audio.wav"
channels = [0, 0, 1, 0]  # Usando o microfone frontal

# Identificar rosto
face_detection.subscribe("Test_face", 500, 0.0)
memValue = "FaceDetected"

# Parar microfone
audio_recorder.stopMicrophonesRecording()

# Loop para ativar chatbot do NAO
n = True
while n:
    # Loop para reconhecer rosto
    rosto_detectado = False
    while not rosto_detectado:
        # Verifica se houve alguma detecção de rosto na memória
        face_data = memoryProxy.getData(memValue)
        
        # Verifica se algum rosto foi detectado
        if face_data and isinstance(face_data, list) and len(face_data) > 0:
            print "Rosto detectado"
            rosto_detectado = True
        else:
            print "Nenhum rosto detectado."

        time.sleep(0.5)

    # Aviso do NAO de reconhecimento
    tts.say("Estou te ouvindo")

    # Silenciar o autofalante (definir volume para 0)
    audio_proxy.setOutputVolume(0)

    # Começar a gravar
    audio_recorder.startMicrophonesRecording(audio_file, "wav", 16000, channels)

    # Aviso de gravação
    print "Gravando."

    # Teste de decibéis
    for i in range(0, 8):
        time.sleep(0.5)
        som = audio_proxy.getFrontMicEnergy()
        print som

    # Parar a gravação
    audio_recorder.stopMicrophonesRecording()

    # Transferir o arquivo para o seu PC e, em seguida, enviá-lo para uma API de transcrição
    os.system("scp nao@{0}:{1} ./".format(ip, audio_file))
    time.sleep(0.5)

    # Para restaurar o volume (ajustar para 100, por exemplo)
    audio_proxy.setOutputVolume(vol_NAO)

    # Ativa o Python 3
    var_resposta = nao_client()
    
    # Retornar
    print "Retornar mensagem do NAO"
    file_path = 'data.json'
    
    # Abrir o arquivo JSON e carregar o conteúdo em uma variável Python (usando codecs para UTF-8)
    try:
        time.sleep(6)
        with codecs.open(file_path, 'r', 'utf-8') as file:
            json_data = json.load(file)
        response = json_data["message"].encode('utf-8')
        tts.say(response)
    except:
        tts.say("Não Entendi")

    if response.lower() == "tchau":
        n = False
