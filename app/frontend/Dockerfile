# Użyj oficjalnego obrazu Pythona jako obrazu bazowego
FROM python:3.11-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki wymagań do katalogu roboczego
COPY requirements.txt ./ 

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj pliki źródłowe aplikacji do katalogu roboczego
# COPY . .

# Ustaw zmienną środowiskową, aby Streamlit nie próbował otworzyć przeglądarki
ENV STREAMLIT_SERVER_PORT=8501

# Informuj Docker, że kontener będzie nasłuchiwał na określonym porcie podczas działania
EXPOSE 8501

VOLUME [ "/app" ]

# Uruchom aplikację Streamlit podczas startu kontenera
CMD ["streamlit", "run", "streamlit_app.py"]