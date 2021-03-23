FROM python:3.7
VOLUME ["/app"]
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python prepare.py
EXPOSE 5000
CMD ["python", "app.py"]