FROM python:3.6.8-slim
WORKDIR /opt/slideviewer3
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /opt/slideviewer3
VOLUME ["/opt/slideviewer3/static/uploads"]
EXPOSE 8080
CMD ["python3", "/opt/slideviewer3/app.py"]
