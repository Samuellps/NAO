import json
import python3

while True:


    #conexão via socket 
    python3.llm_server()

    #puxa a pergunta e roda a llm 
    pergunta = python3.audio_to_text("/home/samuel/Projeto_NAO/gravacao.wav")
    print(pergunta)
    response = python3.consultar_chatgpt(pergunta)
    print(response)

    #limpa o histórico de conversa e fecha a conexão
    if response == "tchau": #condição de parada
        python3.limpar_historico
        python3.socket.close()   
        break


    else:
        # Salvar a string em um arquivo JSON
        file_path = ('data.json')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({"message": response}, file, ensure_ascii=False, indent=4)