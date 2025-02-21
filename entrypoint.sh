#!/bin/bash

# Inicie o tmux
tmux new-session -d -s nao_session

# Ative o ambiente do Python 2.7
tmux send-keys -t nao_session "source /opt/miniconda3/bin/activate env_python2" C-m

# Execute o script Python 2.7
tmux send-keys -t nao_session "python NAO27.py" C-m

# Mantenha o terminal aberto no ambiente do Python 2.7
tmux send-keys -t nao_session "bash" C-m

# Crie uma nova janela para o ambiente do Python 3.12
tmux new-window -t nao_session:1 -n "Python 3.12"

# Ative o ambiente do Python 3.12
tmux send-keys -t nao_session:1 "source /opt/miniconda3/bin/activate env_python3" C-m

# Execute o script Python 3.12
tmux send-keys -t nao_session "python NAO.py" C-m

# Mantenha o terminal aberto
tmux send-keys -t nao_session:1 "bash" C-m

# Anexar ao tmux
tmux attach -t nao_session