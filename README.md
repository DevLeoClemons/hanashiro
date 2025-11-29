# README -- Como Executar o Projeto

Este projeto é um site desenvolvido com **Flask** (framework web em
Python) e utiliza a biblioteca **PyPDF2** para trabalhar com arquivos
PDF.

As instruções abaixo explicam, passo a passo, como instalar e executar o
sistema.

------------------------------------------------------------------------

## 1. Pré-requisitos

Antes de começar, é necessário ter:

### ✔️ Python instalado

Recomendado: **Python 3.10 ou superior**

Para verificar, abra o terminal e digite:

    python --version

ou

    python3 --version

------------------------------------------------------------------------

## 2. Baixar o projeto

1.  Baixe a pasta do projeto para o computador.\
2.  Caso esteja no GitHub, clique em **Code → Download ZIP**.\
3.  Extraia o arquivo.

------------------------------------------------------------------------

## 3. Instalar as dependências

Dentro da pasta do projeto, abra o **terminal** e execute:

    pip install -r requirements.txt

Isso instalará:

-   **Flask**\
-   **PyPDF2**\
-   Outras dependências do projeto

Se não funcionar, tente:

    pip3 install -r requirements.txt

------------------------------------------------------------------------

## 4. Executar o servidor

Na pasta do projeto, execute:

    python app.py

ou

    python3 app.py

Se aparecer algo parecido com:

    Running on http://127.0.0.1:5000/

significa que o servidor iniciou corretamente.

------------------------------------------------------------------------

## 5. Abrir o site

No navegador (Chrome, Edge, Firefox), acesse:

    http://127.0.0.1:5000/

O site vai abrir e estará funcionando.

------------------------------------------------------------------------

## 6. Observações importantes

-   O módulo **typing** já vem com o Python. **Não é necessário
    instalar.**
-   O sistema só funciona enquanto o terminal estiver aberto.\
-   Para encerrar o servidor, pressione **Ctrl + C** no terminal.\
-   Se seu projeto faz upload ou leitura de PDFs, certifique-se de que a
    pasta apropriada existe.
