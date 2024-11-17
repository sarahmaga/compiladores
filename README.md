# Projeto de geração de grafos de fluxo de controle

Este projeto tem como propósito gerar grafos de fluxo utilizando llvm/clang e graphviz.

## Pré-requisitos

Certifique-se de que você tem o Python instalado. Versão utilizada 3.10.6

## Instalação

1. Clone o repositório (ou faça o download do código-fonte):

    ```bash
    git clone https://github.com/sarahmaga/compiladores.git
    cd compiladores
    ```

2. Instale as dependências com o comando abaixo. Isso irá instalar as bibliotecas listadas no arquivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

<!-- 3. Verifique se as bibliotecas foram instaladas corretamente executando o seguinte comando:

    ```bash
    python -c "import pycparser, pydot; print('Bibliotecas instaladas com sucesso!')"
    ``` -->

## Uso

1. Para gerar os dados para um arquivo e específico e para os demais:
    ```bash
    python3 gen_cfg.py caminho/arquivo.c
    ```
---
