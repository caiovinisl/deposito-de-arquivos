# deposito-de-arquivos

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/caiovinisl/deposito-de-arquivos?color=%2304D361">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/caiovinisl/deposito-de-arquivos">
  
  <a href="https://github.com/caiovinisl/metodos-hashing/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/caiovinisl/deposito-de-arquivos">
  </a>
   
   <a href="https://github.com/caiovinisl/metodos-hashing/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/caiovinisl/deposito-de-arquivos?style=social">
  </a>
  
 
</p>

<h4 align="center"> 
	🚧 Depósito de Arquivos 🚧
</h4>

<p align="center">
	<img alt="Status Concluído" src="https://img.shields.io/badge/STATUS-CONCLU%C3%8DDO-brightgreen">
</p>

<p align="center">
 <a href="#-sobre-o-projeto">Sobre</a> •
 <a href="#-funcionalidades">Funcionalidades</a> •
 <a href="#-como-executar-o-projeto">Como executar</a> • 
 <a href="#-tecnologias">Tecnologias</a>
</p>

## 💻 Sobre o projeto

📄 Servidor de arquivos usando sockets.

Projeto desenvolvido durante a matéria MATA59 - Redes de Computadores da Universidade Federal da Bahia pelo professor Gustavo Bittencurt.

A aplicação implementada segue o modelo cliente-servidor e funciona em dois modos:
- i) modo depósito
- ii) modo recuperação

No modo depósito, o cliente informa ao servidor o arquivo a ser armazenado e o nível de tolerância a falhas requerido, que expressa, em última instância a quantidade de réplicas que serão armazenadas. O servidor então guarda as “N” cópias do arquivo em locais (dispositivos) diferentes.

No modo recuperação, o cliente informa o nome do arquivo que deverá ser recuperado. O servidor encontra o arquivo (de alguns dos locais replicados) e devolve ao cliente.

A aplicação mantém a consistência das réplicas. Ou seja, se o cliente mudar o número de replicações para um certo arquivo, o sistema deve
aumenta ou diminui a quantidade de réplicas conforme a última solicitação.

---

## ⚙️ Funcionalidades

- [x] Servidor
- [x] Proxy
- [x] Cliente
  - [x] Depositar arquivos
  - [x] Recuperar arquivos

---

## 🛣️ Como executar o projeto

#### 🎲 Rodando a aplicação

```bash

# Clone este repositório
$ git clone https://github.com/caiovinisl/deposito-de-arquivos.git

# Acesse a pasta do projeto no terminal/cmd
$ cd deposito-de-arquivos

# Certifique-se de executar primeiro o proxy
$ python proxy.py

# Depois execute o servidor
$ python server.py

# Em seguida, execute o cliente
$ python client.py

```

## 🛠 Tecnologias

- **[Python](https://www.python.org/)**

---
