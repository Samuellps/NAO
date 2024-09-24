import json
import python3

while True:


    #conexão via socket 
    python3.llm_server()

    #puxa a pergunta e roda a llm 
    pergunta = python3.audio_to_text("audio.wav")
    print(pergunta)
    response = python3.consultar_chatgpt(pergunta)
    print(response)

    #limpa o histórico de conversa e fecha a conexão
    if response.lower() == "tchau": #condição de parada
        file_path = ('data.json')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({"message": response}, file, ensure_ascii=False, indent=4)
        python3.limpar_historico
        #python3.socket.close()   
        break


    else:
        # Salvar a string em um arquivo JSON
        file_path = ('data.json')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({"message": response}, file, ensure_ascii=False, indent=4)