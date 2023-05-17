# ETL Postgres

Extração do [conjunto da despesa](https://dados.mg.gov.br/dataset/despesa) e carga no PostgreSQL.


## Preparação Ambiente

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

## Instalação e configuração do docker

- Baixar e instalar o Docker Desktop.

### Uso

O arquivo `docker-compose.yml` está configurado para levantar o [PostgreSQL](https://www.postgresql.org/) (usuário: postgres; senha: postgres) e [pgAdmin](https://www.pgadmin.org/) (usuário: splor@planejamento.mg.gov.br; senha: admin). Para isso execute na linha de comando (depois de abrir o Docker Desktop)

```bash
docker compose up
```

O pgAdmin está disponível em <http://localhost:5050/>. É necessário inserir a senha default `postgres` para conexão ao banco.

Se o cliente `psql` estiver instalado é possível se conectar ao banco de dados com:

```bash
psql -h localhost -U postgres -W
```

## Execução no Python

- Ativar o ambiente virtual (caso já não esteja ativado)

- Executar makefile

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

