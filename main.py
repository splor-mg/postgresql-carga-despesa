import pandas as pd
import glob
import os
import psycopg2
from sqlalchemy import create_engine
import time
import frictionless
from config import remove_path_redundancies, dtypes_from_datapackage

DB_NAME = 'dadosmg'
DATASETS_DIR = 'despesa/'
DATASET_DIR = 'datasets/'
DATA_DIR = 'data/'
DATA_PATH = DATASET_DIR + DATASETS_DIR + DATA_DIR

# obtem lista de paths para arquivos CSV localizados no caminho DATA_PATH
file_paths = [i.replace('\\', '/') for i in list(glob.iglob(f'{DATA_PATH}*.csv*'))]



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

def create_database(database_name):
    """
        Creates a database with the given name, if not exists already.

        :param database_name: Name of the database to be created.
        :return: none.
    """
    con = psycopg2.connect("user=postgres password=postgres")
    con.autocommit = True # To avoid the need of rollbacks
    cur = con.cursor()
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {database_name}")

    con.autocommit = False
    con.commit()
    cur.close()
    con.close()


def tables_from_csv(package, connection_string):
    """
        Reads csv files and create one table with them.

        :param file_paths: list of complete paths to each csv file.
        :param con: connection object to the database.
        :return: none.
    """

    db = create_engine(connection_string)
    conn = db.connect()

    for resource in package.resources:

        #resource = package.get_resource(name)
        file = remove_path_redundancies(resource)
        print(f"Lendo {file}")
        df = pd.read_csv(file, delimiter=';', decimal='.')
        df = dtypes_from_datapackage(resource, df)

        # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
        df.to_sql(resource.name, conn, if_exists='replace', index=False, )
        print(f"Arquivo {file} carregado para tabela {resource.name}\n")
        conn.commit()

    print('-------------------------------------------------------\n')

def append_from_csv(package, connection_string, tbl_agg_name):
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

    # postgres_engine = create_engine(f"postgresql+psycopg2://postgres:postgres@localhost/{DB_NAME}")

    db = create_engine(connection_string)
    conn = db.connect()

    for resource in package.resources:

        file = remove_path_redundancies(resource)
        print(f"Lendo arquivo {file}")
        df = pd.read_csv(file, delimiter=';', decimal='.')
        df = dtypes_from_datapackage(resource, df )

        # try:
        # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
        df.to_sql(tbl_agg_name, conn, if_exists='append', index=False, )
        conn.commit()
        print(f"Arquivo {file} concatenado na tabela {tbl_agg_name}\n")
        num_linhas += len(df)

    print('-------------------------------------------------------\n')

    #except:
        # print(f"ERRO: Arquivo {file} está vazio ou contém schema divergente dos demais.\n")
        # exec_error = True
        # files_error.append(file)

    print('-------------------------------------------------------')

    print('Total de linhas das tabelas lidas:', num_linhas)

    # Alerta para falha no carregamento de arquivos. Arquivos somente com cabeçalhos geram esse erro.
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



if __name__ == '__main__':

    start_time = time.time()

    create_database(DB_NAME)

    con = psycopg2.connect(user="postgres",
                         password="postgres",
                         database=DB_NAME)

    connection_string = f"postgresql+psycopg2://postgres:postgres@localhost/{DB_NAME}"
    package = frictionless.Package('datasets/despesa/data/datapackage.json')

    # paths de bases csv que sao separadas por anos
    resources_desp = [package.get_resource(x) for x in package.resource_names if "dm_empenho_desp_" in x]
    resources_ft = [package.get_resource(x) for x in package.resource_names if "ft_despesa_" in x]

    # paths de bases csv que não são separadas por anos
    singleTable_resources = [r for r in package.resources if r not in resources_desp and r not in resources_ft]

    singleTable_resources = frictionless.Package(resources=singleTable_resources)
    resources_desp = frictionless.Package(resources=resources_desp)
    resources_ft = frictionless.Package(resources=resources_ft)

    if DROP_TABLES:
        drop_tables(con)

    tables_from_csv(singleTable_resources, connection_string)

    append_from_csv(resources_desp, connection_string, 'dm_empenho_desp')
    append_from_csv(resources_ft, connection_string, 'ft_despesa')


    end_time = time.time()

    print(f"Tempo Total de execução: {end_time - start_time}")
