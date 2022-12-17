from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta

default_args = {
    'owner': 'iliaklop',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(dag_id="create_datamart", default_args=default_args, start_date=datetime.today(),
          schedule_interval='@monthly', catchup=False)
task1 = PostgresOperator(task_id='missions_names', postgres_conn_id="postgres_localhost",
                         sql="""create table if not exist DMMissionNames (mission_id text,
                                          launch_id integer,
                                          m_mission_name text,
                                          l_mission_name text);""", dag=dag)
task2 = PostgresOperator(task_id='fill_in', postgres_conn_id="postgres_localhost",
                         sql="""INSERT INTO DMMissionNames (
select jm.mission_id as mission_id, l.id as launch_id, jm.mission_name as m_mission_name, l.mission_name as l_mission_name
from (missions m inner join launch_missions lm on m.id==lm.mission_id) jm inner join launches l on jm.launch_id==l.id);""",
                         dag=dag)

task1 >> task2

