# NAO
Repositório dedicado ao estudo e desenvolvimento de interações com o robô NAO, usando diferentes versões de Python para realizar processamento de linguagem natural (NLP).

Visão Geral

O projeto conecta o robô NAO a um modelo de linguagem GPT, permitindo que o robô grave áudio com seu microfone, transcreva-o, envie para uma API de modelo de linguagem e depois fale a resposta.

O fluxo é feito usando Python 2.7 (para o controle do NAO) e Python 3.12 (para a interação com o modelo de linguagem), utilizando sockets para comunicação entre as duas versões.

Pré-requisitos:

Python 2.7 (para controle do NAO)

Python 3.12 (para interação com a API do GPT)

NAO SDK e NAOqi

Bibliotecas:

socket

Google Cloud Speech API

OpenAI

JSON

Fluxo de Dados:

1 - O áudio é gravado pelo microfone do NAO usando a API do NAOqi.

2 - Esse áudio é processado por uma biblioteca de transcrição (s2t) no Python 3.12.

3 - A transcrição é enviada para a API GPT, que retorna uma resposta.

4 - A resposta é enviada de volta ao Python 2.7 para que o NAO possa falar.
