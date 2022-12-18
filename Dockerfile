FROM apache/airflow:2.4.3
RUN python -m pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
COPY app/app.py /opt/iliaklop/app/app.py
COPY app/config.py /opt/iliaklopapp/config.py
COPY app/model.py /opt/iliaklopapp/model.py
CMD ["python", "-u", "app/app.py"]
