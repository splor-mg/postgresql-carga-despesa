# Pipeline Postgres

Extração do [conjunto da despesa](https://dados.mg.gov.br/dataset/despesa) e carga no PostgreSQL.

## Instalação e configuração do docker

- Docker Desktop

## Uso

O arquivo `docker-compose.yml` está configurado para levantar o [PostgreSQL](https://www.postgresql.org/) (usuário: postgres; senha: postgres) e [pgAdmin](https://www.pgadmin.org/) (usuário: splor@planejamento.mg.gov.br; senha: admin). Para isso execute na linha de comando (depois de abrir o Docker Desktop)

```bash
docker compose up
```

O pgAdmin está disponível em <http://localhost:5050/>. É necessário inserir a senha default `postgres` para conexão ao banco.

Se o cliente `psql` estiver instalado é possível se conectar ao banco de dados com:

```bash
psql -h localhost -U postgres -W
```


## Instalação e execução do código no Windows

Selecionar o branch (main para versão já revisada ou development para versão em desenvolvimento):

Git bash:
```gitbash
git checkout -b <branch> --track origin/<branch>
```

Clonar o projeto, seguir as etapas a seguir.


### Criar ambiente virtual do projeto
```python
cd diretorio/do/projeto
python -m venv venv
```

### Ativar ambiente virtual do projeto

Linha de comando no Windows:
```cmd
cd diretorio/do/projeto
venv\Scripts\activate
```

Git bash:
```gitbash
cd diretorio/do/projeto
source venv\Scripts\activate
```

### Instalar requerimentos
```python
pip install -r requirements.txt
```

### Instalar Jupyter Notebook (opcional)
```python
pip install notebook
```

## Execução no Python

### Ativar o ambiente virtual (caso já não esteja ativado)

Linha de comando no Windows:
```cmd
cd diretorio/do/projeto
venv\Scripts\activate
```

Git bash:
```gitbash
cd diretorio/do/projeto
source venv\Scripts\activate
```

### Executar makefile

Baixar arquivos tar.gz do portal dadosmg:  
```python
make download
```

Executar script de carga de dados:  
```python
make run
```

Fazer download dos arquivos e executar o script de carga de dados:
```python
make all
```

## Execução no Jupyter Notebook

Ativar o ambiente virtual:
```gitbash
cd diretorio/do/projeto
source venv\Scripts\activate
```

Baixar os arquivos csv.gz do portal [dadosmg](https://dados.mg.gov.br/dataset/despesa), salvá-los na pasta \datasets e extrair todos os arquivos csv. Após isso abrir o notebook 'dadosmg_basics.ipynb' no jupyter e executar.  