# SpaceX_datamart
Task:

- Write any script, that load data from [GraphQL API](https://studio.apollographql.com/public/SpaceX-pxxbxen/home) to any to relational database of your choice
- Design some base layer of datamarts for analysts
- Write scripts to fill your datamarts with data
- Create datamart, that calculates number of publications for missions, rockets and launches
- Describe Dockerfile and write docker-compose.yml file, that will allow us to run your code and query your RDBMS (`docker-compose build и up`)

## Описание проекта
1. Приложение выгружает часть массива данных SpaceX по GraphQL API (только часть массива данных, т.к. проект создавался под конкретную задачу в условиях ограниченного времени) и складывает в базу данных PostgreSQL с использованием ORM модели и добавлением служебных полей даты загрузки.
2. Контейнер datamarts строит витрины данных. В текущей реализации добавлены 4 витрины, без возможности оркестрации и апдейта расчитанных ранее данных. Только единоразовый расчет. В дальнейшем возможно добавление оркестрации в airflow, а также возможность апдейта данных.

3. В ветке develop выложена другая версия проекта. С немного другой структурой, включающей airflow и возможностью апдейта расчитанных ранее витрин. На текущий момент реализованы витрины dm_missions и dm_publications. 

