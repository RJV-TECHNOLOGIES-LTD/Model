FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "execution.py"]

EXPOSE 8080
