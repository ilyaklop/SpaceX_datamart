from sqlalchemy import create_engine
from config import DB_NAME, USER, PASS, HOST, PORT
from sqlalchemy.exc import IntegrityError
import psycopg2
import psycopg2.extras

import logging

logger = logging.getLogger(__name__)
spaceX_engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USER, PASS, HOST, PORT,  DB_NAME))


def mission_names(engine):
    """Тестовая витрина. Название миссии может изменятся от запуска к запуску - собираем все названия"""
    try:
        create_table_sql = """create table if not exists dm_mission_names (mission_id text,
                                              launch_id integer,
                                              m_mission_name text,
                                              l_mission_name text);
        """
        engine.execute(create_table_sql)
        fill_in_data_sql = """INSERT INTO dm_mission_names (
                                  select lm.mission_id as mission_id, l.id as launch_id, m.name as m_mission_name, 
                                          l.mission_name as l_mission_name
                                  from missions m inner join launch_missions lm on m.id=lm.mission_id inner join 
                                  launches l on lm.launch_id=l.id);"""
        engine.execute(fill_in_data_sql)
    except IntegrityError as e:
        logger.error(e.orig)
    except Exception as e:
        logger.error(e)


def publications(engine):
    """Витрина для отображения публикаций. Так как каждая сущность в основной таблице имеет собственную ссылку на вики,
    было решено посчитать относителльно самой широкой сущности - миссий. А наиболее полные сведения о разного рода
    публикациях имеются для каждого запуска."""
    try:
        create_table_sql = """create table if not exists dm_publications (mission_id text, mission_name text,
                                              m_wiki integer,
                                              n_launches integer,
                                              articles integer,
                                              launches_wiki integer,
                                              video integer,
                                              photos integer);
        """
        engine.execute(create_table_sql)
        fill_in_data_sql = """INSERT INTO dm_publications ( Select m.id as mission_id, m.name as mission_name,
                count(distinct m.wikipedia) as m_wiki,
                count(distinct lm.launch_id) as n_launches,
                count(distinct l.article_link) as articles,
                count(distinct l.wikipedia) as launches_wiki,
                count(distinct l.video_link) as video,
                count(distinct p.flickr_images) as photos
                from missions m left join launch_missions lm on m.id=lm.mission_id left join links l on 
                lm.launch_id=l.launch_id left join launch_photos p on l.launch_id=p.launch_id
                group by m.id, m.name
                order by m.id);"""
        engine.execute(fill_in_data_sql)
    except IntegrityError as e:
        logger.error(e.orig)
    except Exception as e:
        logger.error(e)


def missions_general(engine):
    """Витрина для отображения полной инфы о миссиях. Количество запусков, количесво кораблей(ракет), общая стоимость,
    дата начала, статус, успешные запуски и провальные запуски"""
    try:
        create_table_sql = """create table if not exists dm_missions_general (mission_id text,
                                                                              mission_name text,
                                                                              n_launches integer,
                                                                              n_rockets integer,
                                                                              rockets_cost float,
                                                                              start_date timestamp,
                                                                              status text,
                                                                              success_launches integer,
                                                                              failed_launches integer);
        """
        engine.execute(create_table_sql)
        fill_in_data_sql = """
                            INSERT INTO dm_missions_general ( Select tmp.mission_id as mission_id, 
                            tmp.mission_name as mission_name,
                            count(distinct tmp.launch_id) as n_launches,
                            count(r.rocket_id) as n_rockets,
                            sum(rr.cost_per_launch) as rockets_cost,
                            min(tmp.start_date) as start_date,
                            CASE WHEN count(CASE WHEN tmp.upcoming THEN 1 END) > 0 THEN 'in progress'
                                 WHEN count(CASE WHEN tmp.upcoming THEN 1 END) = 0 THEN 'finished'
                                 ELSE 'unknown'
                            END as status,
                            count(CASE WHEN tmp.launch_success THEN 1 END) as success_launches,
                            count(CASE WHEN tmp.launch_success = FALSE THEN 1 END) as failed_launches
                            from (select m.id as mission_id, m.name as mission_name, l.id as launch_id, 
                          l.launch_success as launch_success, l.upcoming as upcoming, l.launch_date_local as start_date
                          from missions m left join launch_missions lm on m.id=lm.mission_id left join launches l on
                          lm.launch_id=l.id) tmp left join launch_rocket r on tmp.launch_id=r.launch_id left join rockets rr 
                            on r.rocket_id=rr.id
                            group by tmp.mission_id, tmp.mission_name, tmp.upcoming, tmp.launch_success
                            order by tmp.mission_id, min(tmp.start_date));"""
        engine.execute(fill_in_data_sql)
    except IntegrityError as e:
        logger.error(e.orig)
    except Exception as e:
        logger.error(e)


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


if __name__ == "__main__":
    logger.warning("Container alive")
    mission_names(spaceX_engine)
    publications(spaceX_engine)
    missions_general(spaceX_engine)
    try:
        conn = psycopg2.connect(dbname=DB_NAME, host=HOST, user=USER, password=PASS)
        tables = get_tables(conn)
        print("codeinpython Tables\n===================\n")
        print_tables(tables)
        cursor = conn.cursor()
        try:
            cursor.execute("Select * from public.dm_mission_names limit 5;")
            tmp = (cursor.fetchall())
            for i in tmp:
                print(i)
        except Exception as e:
            print('Error: ', e)
        try:
            cursor.execute("Select * from public.dm_publications limit 5;")
            tmp = (cursor.fetchall())
            for i in tmp:
                print(i)
        except Exception as e:
            print('Error: ', e)
        try:
            print("Try to fetch missions_general")
            cursor.execute("Select * from public.dm_missions_general limit 5;")
            tmp = (cursor.fetchall())
            for i in tmp:
                print(i)
        except Exception as e:
            print('Error: ', e)
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(type(e))
        print(e)