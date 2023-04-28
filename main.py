import pandas as pd
import glob
import os
import psycopg2
from sqlalchemy import create_engine
import time

DB_NAME = 'dadosmg'
DATASETS_DIR = 'despesa/'
DATASET_DIR = 'datasets/'
DATA_DIR = 'data/'
DATA_PATH = DATASET_DIR + DATASETS_DIR + DATA_DIR

# obtem lista de paths para arquivos CSV localizados no caminho DATA_PATH
file_paths = [i.replace('\\', '/') for i in list(glob.iglob(f'{DATA_PATH}*.csv*'))]

# paths de bases csv que sao separadas por anos
file_paths_desp = [x for x in file_paths if "dm_empenho_desp_" in x]
file_paths_ft = [x for x in file_paths if "ft_despesa_" in x]

# paths de bases csv que não são separadas por anos
file_paths = list(set(file_paths) - set(file_paths_desp) - set(file_paths_ft))

# True Dropa todas as tabelas atuais da database
DROP_TABLES = True


def drop_tables(con=None):
    """
        Drop all tables from a database.

        :param con: connection object to the database.
        :return: none.
    """
    cur = con.cursor()
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'""")
    res = cur.fetchall()

    if res:
        for table_name in res:
            cur.execute(f"""DROP TABLE {table_name[0]} """)
            print(f"Tabela {table_name} apagada.")
    else:
        print(f"Não há tabelas em {DB_NAME}")

    con.commit()

def tables_from_csv(file_paths, con):
    """
        Reads csv files and create one table with them.

        :param file_paths: list of complete paths to each csv file.
        :param con: connection object to the database.
        :return: none.
    """

    postgres_engine = create_engine(f"postgresql+psycopg2://postgres:postgres@localhost/{DB_NAME}")

    for file in file_paths:
        head, tail = os.path.split(file)
        table_name = tail.split('.')[0]

        df = pd.read_csv(file, delimiter=';', decimal='.')


        # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
        df.to_sql(table_name, postgres_engine, if_exists='replace', index=False, )
        print(f"Arquivo {file} carregado para tabela {table_name}")

    print('-------------------------------------------------------\n')

def append_from_csv(file_paths_append, tbl_agg_name):
    """
        Reads csv files and append in the same table.

        :param file_paths_append: list of complete paths to each csv file.
        :param tbl_agg_name: name of the table that will be created and the data appended
        :return: none.
    """

    df_agg = pd.DataFrame()
    num_linhas = 0
    exec_error = False
    files_error = []
    postgres_engine = create_engine(f"postgresql+psycopg2://postgres:postgres@localhost/{DB_NAME}")

    for file in file_paths_append:
        _, tail = os.path.split(file)
        table_name, file_extension = os.path.splitext(tail)
        print(f'Lendo:', file)

        df = pd.read_csv(file, delimiter=';', decimal='.')

        try:
            df.to_sql(tbl_agg_name, postgres_engine, if_exists='append', index=False)  # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
            print(f"Arquivo {file} concatenado na tabela {tbl_agg_name}\n")
            num_linhas += len(df)
        except:
            print(f"ERRO: Arquivo {file} está vazio ou contém schema divergente dos demais.\n")
            exec_error = True
            files_error.append(file)

    print('-------------------------------------------------------')

    print('Total de linhas das tabelas lidas:', num_linhas)

    # alerta para falha no carregamento de arquivos. Arquivos somente com cabeçalhos geram esse erro.
    if exec_error:
        print(f"ATENÇÃO! os seguintes arquivos não foram carregados para a base de dados:")
        print(files_error, sep='\n')
        print('\n\n')


def show_tables(con=None):
    """
        Show all tables from a database.

        :param con: connection object to the database.
        :return: none.
    """

    cur = con.cursor()
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'""")
    res = cur.fetchall()

    if res:
        print(res)
    else:
        print(f"Não há tabelas na database {DB_NAME}")


    cur.close()


def create_database(database_name):
    """
        Creates a database with the given name, if not exists already.

        :param database_name: Name of the database to be created.
        :return: none.
    """
    con = psycopg2.connect("user=postgres password=postgres")
    con.autocommit = True
    cur = con.cursor()
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {database_name}")

    con.autocommit = False
    cur.close()
    con.close()

if __name__ == '__main__':

    start_time = time.time()

    create_database(DB_NAME)

    con = psycopg2.connect(user="postgres",
                         password="postgres",
                         database=DB_NAME)
    con.autocommit

    show_tables(con)

    if DROP_TABLES:
        drop_tables(con)

    tables_from_csv(file_paths, con)

    append_from_csv(file_paths_desp, 'dm_empenho_desp')
    append_from_csv(file_paths_ft, 'ft_despesa')


    end_time = time.time()

    print(f"Tempo Total de execução: {end_time - start_time} ")
