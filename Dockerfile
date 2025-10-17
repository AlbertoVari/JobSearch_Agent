# ==========================================================
# ✅ STEP 1: Build environment
# ==========================================================
FROM python:3.11-slim AS base

# Disattiva il buffer di output Python per i log immediati
ENV PYTHONUNBUFFERED=1

# Crea directory app
WORKDIR /app

# Copia requirements e installa dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================================
# ✅ STEP 2: Copia file dell’app
# ==========================================================
COPY app.py ./app.py
COPY utils.py ./utils.py
COPY templates ./templates
COPY static ./static

# ==========================================================
# ✅ STEP 3: Configurazione runtime
# ==========================================================
# Espone la porta 8080 (Cloud Run usa questa di default)
EXPOSE 8080

# Variabile d'ambiente per il nome del servizio
ENV PORT=8080

# Avvia il server FastAPI con Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
