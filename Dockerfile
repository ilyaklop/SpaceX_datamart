FROM apache/airflow:2.4.3
RUN python -m pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY app/app.py app/app.py
COPY app/config.py app/config.py
COPY app/model.py app/model.py
CMD ["python", "-u", "app/app.py"]
