# Back-End
Este repositório apresenta o Back-End deste projeto de controle orçamentário.

---
## Como executar 

1. Faça o download dos arquivos.
2. Crie o ambiente virtual.
```
python -m venv env   
```
3.  Inicie o ambiente virtual.
```
.\env\scripts\activate      
```
4.  Instale as libs listadas em `requirements.txt`.
```
(env)$ pip install -r requirements.txt
```
5.  Execute a API.
```
(env)$ flask run --host 0.0.0.0 --port 5000
```
Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
