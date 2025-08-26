# Guia de Configuração do Projeto Django com Docker

Este documento orienta como configurar o ambiente para clonar o repositório via SSH, instalar Docker no Linux e Windows, além de usar Makefiles para facilitar os comandos Docker.

---

## 1. Configurar chave SSH para clonar o repositório

Para evitar digitar usuário e senha toda vez que usar o Git, configure sua chave SSH.

### 1.1 Verificar se já tem uma chave SSH

Abra o terminal e rode:

ls ~/.ssh/id_rsa.pub

### 1.2 Gerar uma nova chave SSH

ssh-keygen -t rsa -b 4096 -C "seu_email@example.com"

### 1.3 Copiar a chave pública

cat ~/.ssh/id_rsa.pub

### 1.4 Adicionar a chave no GitHub

Acesse GitHub > Settings > SSH and GPG keys

Clique em New SSH key

Cole a chave copiada, dê um nome (ex: “PC do <nome>”) e salve.

### 1.5 Testar conexão SSH

ssh -T git@github.com


## 2. Instalar Docker

## 2.1 Linux

### 1. Atualizar pacotes

sudo apt update

### 2. Instalar dependências

sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

### 3. Adicionar chave GPG

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

### 4. Adicionar repositório do Docker

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

### 5. Instalar Docker

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

### 6. Permitir uso sem sudo

sudo usermod -aG docker $USER

### 7. Instalar docker-compose

sudo apt install docker-compose -y

### 8. Testar

docker --version
docker-compose --version
docker run hello-world

## Windows

### 1. Baixar Docker Desktop

https://www.docker.com/products/docker-desktop

### 2. Instalar

Ative "Use WSL 2 instead of Hyper-V".

Reinicie o computador.

### 3. Abrir Docker Desktop

Aguarde até mostrar "Docker is running".

### 4. Testar

docker --version
docker-compose --version
docker run hello-world

# Passo a passo de comandos Git

[Clique aqui](https://chatgpt.com/share/68ae370b-448c-8005-9a2d-c4da5a7a8153) para acessar a página que indica os comandos e passo a passo Git que serão utilizados ao longo do projeto.