import requests
import json

import psycopg2
import psycopg2.extras

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import DB_NAME, USER, PASS, HOST, PORT, QUERY_MISSIONS
from model import Missions, Mission_manufactures, Payloads, Base
from sqlalchemy.orm import sessionmaker
import logging


logger = logging.getLogger(__name__)
spaceX_engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USER, PASS, HOST, PORT,  DB_NAME))
Session = sessionmaker(bind=spaceX_engine)


def call_post(query):
    response = requests.post(url='https://api.spacex.land/graphql/', json={"query": query})
    response.raise_for_status()
    return response


def add_object(class_object, class_name):
    try:
        exist = session.query(class_name).filter(class_name.id == class_object.id).first()
        if exist is None:
            session.add(class_object)
            session.commit()
            #logger.success(f"Created: {class_object}")
        else:
            logger.warning(f"Object already exists in database: {class_object}")
        return exist
    except IntegrityError as e:
        logger.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        logger.error(f"Unexpected error when creating object: {e}")
        raise e


def fill_mission_data(session):
    """Load all data connected with missions"""
    response = call_post(QUERY_MISSIONS)
    mission_item = (entity for entity in json.loads(response.text)['data']['missions'])
    for mission in mission_item:
        payload_data = [Payloads(payload) for payload in mission['payloads'] if payload]
        mission_data = Missions(mission)
        for pld in payload_data:
            add_object(pld, Payloads)
            mission_data.payload_id.append(pld)
        session.add(mission_data)
        session.commit()
        for manufacturer in mission['manufacturers']:
            mis_manu_data = Mission_manufactures(mission['id'], manufacturer)
            session.add(mis_manu_data)
        session.commit()
        session.close()


def fill_rocket_data():
    """Load all data connected with rockets"""
    pass


def fill_launches_data():
    """Load all data connected with launches"""
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

if __name__ == "__main__":
    query_list = [QUERY_MISSIONS]
    Base.metadata.create_all(spaceX_engine)
    session = Session()
    fill_mission_data(session)
    fill_rocket_data()
    fill_launches_data()
    try:
        conn = psycopg2.connect(dbname=DB_NAME, host=HOST, user=USER, password=PASS)#"dbname=codeinpython host='localhost' user='chris' password='chris'"
        tables = get_tables(conn)
        print("codeinpython Tables\n===================\n")
        print_tables(tables)
        cursor = conn.cursor()
        try:
            cursor.execute("Select * from public.missions_payloads")
            tmp = (cursor.fetchall())
            for i in tmp:
                print(i)
        except Exception as e:
            print('Error when MISSIONS: ', e)
        try:
            cursor.execute("Select distinct(id) from public.payloads")
            tmp = (cursor.fetchall())
            for i in tmp:
                print(i)
        except Exception as e:
            print('Error when PAYLOADS', e)
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(type(e))
        print(e)