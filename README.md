# Bem vindo ao Crypto Price


**Stack**
- Linguagem: Python 3.9
- Frameworks: Django, Django-Ninja, Pytest, Poetry
- Infra: Docker, docker-compose

**Instalação**
1. Clone o repositório
2. Execute a pré-instalação
3. Execute a instalação
4. Configure a instância com o .env
6. Execute os testes

```
git clone https://github.com/rvaccari/crypto-price.git && cd crypto-price
make pre-install
make install
make configure
make test
```

**Importando os dados e executando a aplicação**
```
make db-init
make run
curl -X GET  http://127.0.0.1:8000/v1/BRLBTC/mms\?range\=200
```

**Documentação**
```
make run
```
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Executando via docker-compose**
1. Clone o repositório
2. Execute o build
3. Rode o projeto
4. Execute a migração e importação dos dados
5. Pare a execução do projeto
```
git clone https://github.com/rvaccari/crypto-price.git && cd crypto-price
make docker-build
make docker-up
make docker-db-init
make docker-stop
```