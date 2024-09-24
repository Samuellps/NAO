# -*- coding: utf-8 -*-
from naoqi import ALProxy
import os
import time
import socket
import json
import codecs

#criar um socket cliente
def nao_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 6002))  # Conecta ao servidor Python 3
    
    var_ativacao = "ok" #variavel de ativacao
    client_socket.send(var_ativacao.encode()) #ativa o python 3
    response = client_socket.recv(1024).decode('utf-8') #retorna a resposta do python 3

    client_socket.close()
    return response

# Conectar ao NAO
ip = "192.168.1.102"
port = 9559
vol_NAO = 80

#Criacao de Proxy para os modulos
audio_recorder = ALProxy("ALAudioRecorder", ip, port)
face_detection = ALProxy("ALFaceDetection", ip, port)
memoryProxy = ALProxy("ALMemory", ip, port)
tts = ALProxy("ALTextToSpeech", ip, port)
audio_proxy = ALProxy("ALAudioDevice", ip, port)


# Configurar o local onde o arquivo de audio sera salvo no robo
audio_file = "/home/nao/audio.wav"
channels = [0, 0, 1, 0]  # Usando o microfone frontal

#Identificar rosto
face_detection.subscribe("Test_face", 500, 0.0)
memValue = "FaceDetected"

#Parar microfone
audio_recorder.stopMicrophonesRecording()


#Loop para ativar chatbot do NAO
n = True
while n == True:
    
    #Loop para reconhecer rosto
    i=True
    while i == True:
        for i in range(0,20):
            time.sleep(0.5)
            val = memoryProxy.getData(memValue, 0)
            if(val and isinstance(val, list) and len(val) == 2):
                print "Rosto detectado"
                i = False
            

    #Aviso do NAO de reconhecimento
    tts.say("Estou te ouvindo")
    #time.sleep(2)

    # Silenciar o autofalante (definir volume para 0)
    audio_proxy.setOutputVolume(0)

    # Comecar a gravar
    audio_recorder.startMicrophonesRecording(audio_file, "wav", 16000, channels)

    #aviso de gravacao
    print "Gravando."

    # Teste de decibeis
    for i in range(0,8):
        time.sleep(0.5)
        som = audio_proxy.getFrontMicEnergy()
        print som

    # Gravar por um tempo determinado (ex: 6 segundos)
    #time.sleep(4)

    # Parar a gravacao
    audio_recorder.stopMicrophonesRecording()

    # Transferir o arquivo para o seu PC e, em seguida, envia-lo para uma API de transcricao
    os.system("scp nao@{0}:{1} ./".format(ip, audio_file))
    time.sleep(0.5)

    # Para restaurar o volume (ajustar para 100, por exemplo)
    audio_proxy.setOutputVolume(vol_NAO)

    #Ativa o python 3
    var_resposta = nao_client()
    
    #Retornar
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
    