FROM python:latest
WORKDIR /datamarts
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY config.py config.py
COPY create_datamart.py create_datamart.py
CMD ["python", "-u", "create_datamart.py"]