FROM python:3.10

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie pliku z zależnościami i ich instalacja
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie całego kodu aplikacji do obrazu
COPY . .

# Ustawienie zmiennej środowiskowej dla Flask
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development

# Komenda startowa dla kontenera
CMD ["flask", "run", "--host=0.0.0.0"]
