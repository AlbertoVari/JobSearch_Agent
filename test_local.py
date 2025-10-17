"""
Test locale per Job Agent AI
Verifica che:
 - GOOGLE_API_KEY e GOOGLE_CSE_ID siano impostati
 - Google Custom Search risponda correttamente
 - Ranking intelligente funzioni
"""

import os
from utils import google_job_search, get_salary_benchmark, rank_jobs

# -------------------------------------------------------
# 1️⃣ Imposta variabili d'ambiente (solo per test locale)
# -------------------------------------------------------
# Inserisci qui le tue chiavi temporaneamente (o esportale in shell)
# os.environ["GOOGLE_API_KEY"] = "LA_TUA_API_KEY"
# os.environ["GOOGLE_CSE_ID"] = "IL_TUO_CSE_ID"

# -------------------------------------------------------
# 2️⃣ Definizione parametri di ricerca
# -------------------------------------------------------
role = "SAP"
location = "Milano, Italia"
years = 5

print(f"🔍 Ricerca di: {role} @ {location}\n")

# -------------------------------------------------------
# 3️⃣ Esegui ricerca su Google
# -------------------------------------------------------
jobs = google_job_search(role, location, max_results=10)

if not jobs:
    print("❌ Nessun annuncio trovato (verifica chiave API e CSE ID).")
    exit(1)

print(f"✅ Trovati {len(jobs)} annunci.\n")

# -------------------------------------------------------
# 4️⃣ Benchmark e ranking
# -------------------------------------------------------
benchmark = get_salary_benchmark(role, location, years)
ranked = rank_jobs(jobs, benchmark, location)

# -------------------------------------------------------
# 5️⃣ Mostra risultati
# -------------------------------------------------------
print("🏆 Classifica (Top 5)\n")
for i, r in enumerate(ranked[:5], start=1):
    job = next((j for j in jobs if j["apply_url"] == r["apply_url"]), {})
    print(f"{i}. {job.get('title', 'N/D')}")
    print(f"   🔗 {job.get('apply_url', 'N/A')}")
    print(f"   💰 RAL stimata: {job.get('salary_estimated', 'N/A')}")
    print(f"   📍 Fonte: {job.get('source', 'N/A')}")
    print(f"   🧠 Punteggio: {r['score']} / 100")
    print(f"   📊 {r['rationale']}\n")

print("✅ Test completato con successo!")
