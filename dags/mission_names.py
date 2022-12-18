from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


from datetime import datetime, timedelta

default_args = {
    'owner': 'iliaklop',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(dag_id="mission_names", default_args=default_args, start_date=datetime.today(),
          schedule_interval='@monthly')


task1 = PostgresOperator(task_id='create', postgres_conn_id="postgres_localhost",
                         sql="""create table if not exists dm_mission_names (mission_id text,
                                              launch_id integer,
                                              m_mission_name text,
                                              l_mission_name text,
                                              load_date timestamp);""", dag=dag)

#Эта витрина не требует обновления уже записанных данных. Зостаточно вставить Запуски, загруженные после даты последнего
#обновления. Витрина расчитывается в день загрузки новых данных.
task2 = PostgresOperator(task_id='fill_in', postgres_conn_id="postgres_localhost",
                         sql="""INSERT INTO dm_mission_names (
                                  select lm.mission_id as mission_id, l.id as launch_id, m.name as m_mission_name, 
                                          l.mission_name as l_mission_name, current_date as load_date
                                  from missions m inner join launch_missions lm on m.id=lm.mission_id inner join 
                                  launches l on lm.launch_id=l.id
                                  WHERE l.load_date=to_date('{{ ds }}',  'YYYY-MM-DD'));""",
                         parameters={"prev_date": "{{ prev_ds }}"}, dag=dag)

task1 >> task2
