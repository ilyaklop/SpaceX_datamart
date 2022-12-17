from sqlalchemy import create_engine
from config import DB_NAME, USER, PASS, HOST, PORT
import psycopg2
import psycopg2.extras

import logging

logger = logging.getLogger(__name__)
spaceX_engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USER, PASS, HOST, PORT,  DB_NAME))
#Session = sessionmaker(bind=spaceX_engine)


def mission_names(engine):
    """Тестовая витрина. Названия миссий могут изменятся от запуска к запуску - собираем все названия"""
    create_table_sql = """create table if not exist DMMissionNames (mission_id text,
                                          launch_id integer,
                                          m_mission_name text,
                                          l_mission_name text);
    """
    engine.execute(create_table_sql)
    fill_in_data_sql = """INSERT INTO DMMissionNames (
                          select jm.mission_id as mission_id, l.id as launch_id, jm.mission_name as m_mission_name, 
                                  l.mission_name as l_mission_name
                          from (missions m inner join launch_missions lm on m.id==lm.mission_id) jm inner join 
                          launches l on jm.launch_id==l.id);"""
    engine.execute(fill_in_data_sql)


def publications(engine):
    """Витрина для отображения публикаций"""
    create_table_sql = """create table if not exist DMPublications (mission_id text,
                                          n_launches integer
                                          articles integer
                                          wiki integer,
                                          video integer,
                                          photos integer);
    """
    engine.execute(create_table_sql)
    fill_in_data_sql = """INSERT INTO DMPublications (
                          );"""
    engine.execute(fill_in_data_sql)


def top_missions(engine):
    """Витрина для отображения полной инфы о миссиях. Количество запусков, количесво кораблей(ракет), общая стоимость,
    общая продолжительность, успех"""
    pass

def get_tables(connection):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""SELECT table_schema, table_name
                      FROM information_schema.tables
                      WHERE table_schema != 'pg_catalog'
                      AND table_schema != 'information_schema'
                      AND table_type='BASE TABLE'
                      ORDER BY table_schema, table_name""")

    tables = cursor.fetchall()
    cursor.close()
    return tables


def print_tables(tables):
    for row in tables:
        print("{}.{}".format(row["table_schema"], row["table_name"]))


if __name__ == "__maine__":
    logger.warning("Container alive")
    try:
        mission_names(spaceX_engine)
        logger.info("Table DMMissionNames was created successfully")
    except Exception as e:
        logger.info("Table DMMissionNames was failed: ", e)

    try:
        conn = psycopg2.connect(dbname=DB_NAME, host=HOST, user=USER, password=PASS)#"dbname=codeinpython host='localhost' user='chris' password='chris'"
        tables = get_tables(conn)
        print("codeinpython Tables\n===================\n")
        print_tables(tables)
        cursor = conn.cursor()
        try:
            cursor.execute("Select * from public.DMMissionNames")
            tmp = (cursor.fetchall())
            for i in tmp:
                print(i)
        except Exception as e:
            print('Error when MISSIONS: ', e)
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(type(e))
        print(e)