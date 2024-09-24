import speech_recognition as sr
from openai import OpenAI
import socket


#Define o comportamento do chat e armazena as informações da conversa
historico = [{"role": "system", "content": "Você é um robô chamado NAO. Se o usuário se despedir de você, responda somente com 'tchau' e NADA além disso "}]


def llm_server():
    """FUNÇÃO QUE ESTABELECE CONEXÃO COM O NAO ATRAVÉS DE UM SOCKET SERVIDOR."""


    #cria e configura o servidor socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 6000))  # Abre o servidor na porta 6000
    server_socket.listen(1)
    print("Servidor aguardando conexões")


    #aguarda a conexão com o  NAO
    conn, addr = server_socket.accept()
    print(f"Connected to: {addr}")


    #sinal de ativação
    var_ativacao = conn.recv(1024).decode()
    print(f"Received from Python 2.7: {var_ativacao}")


    var_resposta = ('ok')
    conn.send(var_resposta.encode('utf-8'))



def audio_to_text(audio_file):
    """FUNÇÃO QUE TRANSFORMA UM ARQUIVO DE ÁUDIO WAV EM TEXTO
    PARÂMETRO = ARQUIVO DE ÁUDIO
    SAÍDA = TEXTO TRANSCRITO
    """

    #Cria o objeto que realiza o reconhecimento
    r = sr.Recognizer()


    # Carrega o arquivo de áudio
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)


    try:
        # Realiza o reconhecimento de fala
        text = r.recognize_google(audio, language='pt-BR')  # Substitua 'pt-BR' pelo idioma desejado
        return text
    

    #tratamentos de erros
    except sr.UnknownValueError:
        print("Não foi possível reconhecer o áudio")
    except sr.RequestError as e:
        print("Erro do serviço de reconhecimento de fala; {0}".format(e))




def consultar_chatgpt(texto):
    """FUNÇÃO QUE CHAMA O CHAT, ENTREGA O PROMPT E ARMAZENA TANTO A RESPOSTA QUANTO A PERGUNTA
    PARÂMETRO = TEXTO COLETADO PELA FUNÇÃO AUDIO_TO_TEXT
    SAÍDA = RESPOTA DO CHAT GPT
    """

    #inicia o cliente da API através da chave de api
    client = OpenAI(api_key="CHAVE_API!")


    #armazena o texto entregue como parâmetro como contéudo enviado pelo usuário
    historico.append({"role": "user" , "content": texto})


    #define o modelo do chat e utiliza o "histórico" como contexto
    response = client.chat.completions.create(
    model="gpt-4o",
    messages= historico)


    #responde a mensagem considerando o contexto
    resposta_chatgpt = response.choices[0].message.content


    #armazena a resposta do chat como contéudo enviado pelo assistente (próprio chat)
    historico.append({"role": "assistant", "content": resposta_chatgpt})
    return resposta_chatgpt




def limpar_historico():
    """FUNÇÃO QUE RESETA  HISTÓRICO DO CHAT PARA O PADRÃO"""


    global historico  # Usando 'global' para modificar a variável global
    historico = [{"role": "system", "content": "Você é um robô chamado NAO e seu objetivo é interagir com pessoas importantes em eventos sobre tecnologia."}]
