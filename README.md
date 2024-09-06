# Desafio-Meliuz
Repositório com o código do desafio para vaga Méliuz

## Introdução
Este projeto foi desenvolvido para ajudar a **xpto.com.br** a conter a queda no faturamento mensal, oferecendo recomendações de produtos para novos usuários com base no crescimento de vendas e na receita total.

## Configuração

### 1. Clonando o Repositório e Baixando Arquivos Necessários

1.1 Clone o repositório:
    ```
    git clone https://github.com/felipefraxe/Desafio-Meliuz.git
    ```
    ```
    cd Desafio-Meliuz
    ```

1.2 Faça o download do arquivo `src/data/xpto_sales_products_mar_may_2024.csv` (disponível no documento pdf do case), coloque-o na pasta `src/data/`, a partir da raiz do projeto.


### 2. Ativando o container Docker
2.1 Ative o container docker com o serviço da api:
    ```
    docker compose up -d
    ```

2.2 Abra seu navegador e faça requisições http:
    ```
    http://localhost:5000/recommend/1
    ```

### 3. Executando os testes
3.1 Em seu terminal, entre no container através do comando:
    ```
    docker exec -it desafio-meliuz-api-1 bash
    ```
3.2 Execute os comandos:
    ```
    pytest tests/services/product.py
    ```

    ```
    pytest tests/models/product.py
    ```

## Estrutura de Arquivos e Diretórios
- `docs/`: Arquivo pdf com a documentação do projeto
- `compose.yaml` e `Dockerfile`: Configuração do serviço Docker.
- `README.md`: Instruções do projeto.
- `requirements.txt`: Dependências do Python.
- `tests`: Diretório contendo testes unitários.
- `src/`: Diretório raíz referente ao funcionamento da API.
- `src/data/`: Armazena arquivo xpto_sales_products_mar_may_2024.csv.
- `src/app.py`: Script principal da API flask.