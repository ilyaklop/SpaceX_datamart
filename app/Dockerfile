FROM python:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py app.py
COPY config.py config.py
COPY model.py model.py
EXPOSE 8000
CMD ["python", "-u", "app.py"]