# Pipeline Postgres

Extração do [conjunto da despesa](https://dados.mg.gov.br/dataset/despesa) e carga no PostgreSQL.

## Instalação e configuração

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
