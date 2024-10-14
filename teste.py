from naoqi import ALProxy
import time


# Conectar ao NAO
ip = "192.168.1.103"
port = 9559

# Conecte-se ao NAO
lifeProxy = ALProxy("ALAutonomousLife", ip, port)

# Ativar o Autonomous Life no modo 'social'
lifeProxy.setState("solitary")  # ou "interactive" para mais interacao

# Opcional: verificar o estado atual
state = lifeProxy.getState()
print state