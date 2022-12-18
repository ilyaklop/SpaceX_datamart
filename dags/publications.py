from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)
default_args = {
    'owner': 'iliaklop',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(dag_id="publications", default_args=default_args, start_date=datetime.today(),
          schedule_interval='@monthly')


def update_publications(curr_date):
    """Здесь Если нашлись новые запуски и публикации к ним, то нужно обновить количество для соответствующей миссии"""
    p_conn = PostgresHook(postgres_conn_id="postgres_localhost").get_conn()
    cursor = p_conn.cursor()
    query_all = """Select m.id as mission_id, m.name as mission_name,
                count(distinct m.wikipedia) as m_wiki,
                count(distinct lm.launch_id) as n_launches,
                count(distinct l.article_link) as articles,
                count(distinct l.wikipedia) as launches_wiki,
                count(distinct l.video_link) as video,
                count(distinct p.flickr_images) as photos,
                current_date as load_date
                from missions m left join launch_missions lm on m.id=lm.mission_id left join links l on 
                lm.launch_id=l.launch_id left join launch_photos p on l.launch_id=p.launch_id
                group by m.id, m.name
                order by m.id"""

    query_already = """select mission_id from dm_publications"""
    try:
        cursor.execute(query_already)
        exist_data = [cursor.fetchall()]
        logger.warning('Exist_data: ', exist_data)
        cursor.execute(query_all)
        gen = (cursor.fetchall())
        #item = (mission_id , mission_name, m_wiki, n_launches, articles, launches_wiki, video, photos, load_date)
        #            0            1             2          3        4            5         6      7        8
        for item in gen:
            if item[0] in exist_data:
                logger.warning("I'm in update branch")
                update_string = f"""UPDATE ONLY dm_publications SET m_wiki = {item[2]}, 
                n_launches = {item[3]}, articles = {item[4]}, launches_wiki = {item[5]},
                video = {item[6]}, photos = {item[7]}, load_date = {curr_date}
                where mission_id={item[0]}"""
                cursor.execute(update_string)
            else:
                logger.warning("I'm in insert branch")
                insert_string = f"""INSERT INTO dm_publications VALUES('{item[0]}', '{item[1]}', {item[2]}, {item[3]},
                                {item[4]},{item[5]},{item[6]}, {item[7]},'{item[8].strftime('%Y-%m-%d %H:%M:%S')}')"""
                cursor.execute(insert_string)
            p_conn.commit()
    except Exception as e:
        logger.error(e)


task1 = PostgresOperator(task_id='create', postgres_conn_id="postgres_localhost",
                         sql="""create table if not exists dm_publications (mission_id text, mission_name text,
                                              m_wiki integer,
                                              n_launches integer,
                                              articles integer,
                                              launches_wiki integer,
                                              video integer,
                                              photos integer,
                                              load_date timestamp);""", dag=dag)


task2 = PythonOperator(task_id='fill_in', python_callable=update_publications,
                       op_kwargs={'curr_date': "{{ ds }}"}, dag=dag)

task1 >> task2
