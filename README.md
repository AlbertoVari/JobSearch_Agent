# JobSearch_Agent - Agente AI per la Ricerca Lavoro
JobSearch Agent è un'applicazione AI-based sviluppata in FastAPI, progettata per cercare automaticamente offerte di lavoro da fonti online (LinkedIn, Indeed, Glassdoor, ecc.) utilizzando Google Custom Search API.


L’applicazione permette di specificare:

Ruolo o posizione lavorativa

Località

Anni di esperienza

e restituisce una lista di offerte reali, analizzate e ordinate in modo intelligente in base alla pertinenza, seniority e qualità del contenuto.

L’interfaccia è moderna e reattiva, costruita con Bootstrap, e ospitata su Google Cloud Run come servizio serverless.

✨ Funzionalità principali

✅ Ricerca intelligente
L’agente formula query dinamiche su Google Custom Search, filtrando i risultati più rilevanti da siti affidabili (LinkedIn, Glassdoor, Indeed).

✅ Estrazione automatica dei dati
Analizza i titoli, snippet e località per identificare le informazioni principali di ogni offerta (titolo, azienda, sede, link diretto).

✅ Ranking AI-based
Ogni offerta riceve un punteggio di pertinenza basato su:

Rilevanza della posizione

Seniority del ruolo (es. “Senior”, “Lead”, “Manager” → punteggio più alto)

Distanza o possibilità di lavoro “remote”

✅ Interfaccia web moderna
UI responsive con Bootstrap 5, semplice e intuitiva:

Form di ricerca (ruolo + località)

Tabella risultati dinamica e ordinata per punteggio

✅ Deploy serverless su Google Cloud Run

Auto-scaling gestito da Google

Nessun server da mantenere

Log accessibili direttamente da Cloud Console

🧩 Architettura
Componente	Tecnologia	Descrizione
Backend API	FastAPI (Python 3.11)	Gestione richieste, logica business e integrazioni
Frontend	Jinja2 + Bootstrap	Rendering HTML dinamico lato server
AI Ranking	Regole euristiche su testo	Punteggio per pertinenza e seniority
Search Engine	Google Custom Search API	Recupero offerte reali dal web
Hosting	Google Cloud Run	Deploy container serverless
Build system	Cloud Build + Docker	Pipeline CI/CD integrata
🏗️ Struttura del progetto
job-agent/
│
├── app.py                  # Entry point principale FastAPI
├── utils.py                # Funzioni di supporto (parsing, ranking)
├── requirements.txt        # Dipendenze Python
├── Dockerfile              # Configurazione container per Cloud Run
│
├── templates/
│   └── index.html          # Template principale con UI Bootstrap
│
└── static/
    └── style.css           # Stili personalizzati

⚙️ Setup locale
1️⃣ Clona il repository
git clone https://github.com/<tuo-utente>/jobsearch-agent.git
cd jobsearch-agent

2️⃣ Installa le dipendenze
pip install -r requirements.txt

3️⃣ Imposta le variabili d’ambiente
export GOOGLE_API_KEY="la_tua_api_key"
export GOOGLE_CSE_ID="il_tuo_cse_id"

4️⃣ Avvia in locale
uvicorn app:app --reload


➡️ Poi apri http://localhost:8000

☁️ Deploy su Google Cloud Run
Build dell’immagine
gcloud builds submit --tag gcr.io/<PROJECT_ID>/jobagent-ui

Deploy del servizio
gcloud run deploy jobagent-ui \
  --image gcr.io/<PROJECT_ID>/jobagent-ui \
  --region us-central1 \
  --allow-unauthenticated


Cloud Run si occuperà di scalare automaticamente il servizio in base al traffico.

🧠 Esempio di utilizzo
Input	Output
Ruolo: “Python Developer”
Località: “Milano”	🔍 L’agente effettua una ricerca tramite Google Custom Search e restituisce una lista ordinata di offerte con link diretti.
Ruolo: “Project Manager”
Località: “Roma”	🔍 Vengono mostrate le offerte più pertinenti, con punteggio basato su seniority e distanza.
🔐 Configurazione Google Custom Search

Crea una Custom Search Engine (CSE) su https://cse.google.com

Imposta i domini consentiti (es. linkedin.com, glassdoor.com, indeed.com)

Recupera il tuo CX ID e API Key da Google Cloud Console

🧾 Requisiti
Libreria	Versione minima
fastapi	0.115.2
uvicorn	0.30.1
requests	2.32.3
jinja2	3.1.4
python-multipart	0.0.9
google-cloud-secret-manager	2.21.0
👨‍💻 Autore


App AI sviluppata per la ricerca intelligente di opportunità di lavoro, basata su tecnologie cloud e intelligenza artificiale.

🧩 Licenza

Distribuito sotto licenza MIT — libero utilizzo, modifica e distribuzione con attribuzione.
