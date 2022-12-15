import requests
import json

from sqlalchemy import create_engine
from config import DB_NAME, USER, PASS, HOST, PORT, QUERY_MISSIONS
from model import Missions, Mission_manufactures, Payloads, Base
from sqlalchemy.orm import sessionmaker

spaceX_engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USER, PASS, HOST, PORT,  DB_NAME))
Session = sessionmaker(bind=spaceX_engine)


def call_post(query):
    response = requests.post(url='https://api.spacex.land/graphql/', json={"query": query})
    response.raise_for_status()
    return response


if __name__ == "__main__":
    query_list = [QUERY_MISSIONS]
    Base.metadata.create_all(spaceX_engine)
    session = Session()
    for query in query_list:
        response = call_post(query)
        mission_item = (entity for entity in json.loads(response.text)['data']['missions'])
        for mission in mission_item:
            payload_data = [Payloads(payload) for payload in mission['payloads'] if payload]
            mission_data = Missions(mission)
            mission_data.payload_id = payload_data
            session.add(mission_data)
            session.commit()
            for manufacturer in mission['manufacturers']:
                mis_manu_data = Mission_manufactures(mission['id'], manufacturer)
                session.add(mis_manu_data)
            session.commit()
            session.close()

