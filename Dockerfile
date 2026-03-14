# Használjunk egy hivatalos, könnyűsúlyú Python alapképet
FROM python:3.11-slim

WORKDIR /app

# Függőségek másolása és telepítése
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# A projekt többi fájljának átmásolása
COPY . .

# Biztosítjuk, hogy az uploads mappa és a Flask instance mappa létezzen
RUN mkdir -p uploads instance

# Az 5000-es port kiajánlása
EXPOSE 5000

# Az alkalmazás indítása (0.0.0.0 host kell, hogy kívülről is elérjük)
CMD ["flask", "run", "--host=0.0.0.0"]