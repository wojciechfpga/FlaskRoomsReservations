FROM python:3.10
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]
