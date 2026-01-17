# Dockerfile für Dandelions Bot (Cloud Deployment)
FROM python:3.11-slim

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# 1. Abhängigkeiten installieren
# Kopiere zuerst die requirements.txt aus dem Unterordner
COPY dandelions/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 2. Anwendungscode kopieren
# Kopiere den gesamten Inhalt des 'dandelions' Unterordners
COPY dandelions/ /app/

# 3. Container starten
# Startet das einfache Bot-Skript (ändern, wenn du ai_bot.py nutzen willst)
CMD ["python", "simple_bot.py"]
