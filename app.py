from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import re
import os
from datetime import datetime

app = FastAPI()

# === CONFIG ===
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# === UTILS ===

def fetch_job_listings(role: str, location: str, limit: int = 10):
    """Cerca offerte di lavoro tramite Google Custom Search API"""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("❌ API key o CSE ID non impostati.")
        return []

    query = f"{role} {location} lavoro site:linkedin.com OR site:glassdoor.com OR site:indeed.com"
    url = (
        f"https://www.googleapis.com/customsearch/v1?q={query}"
        f"&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    )

    try:
        resp = requests.get(url)
        data = resp.json()
        results = []

        for item in data.get("items", [])[:limit]:
            title = item.get("title", "Senza titolo")
            link = item.get("link", "#")
            snippet = item.get("snippet", "")
            company = re.search(r"presso\s+([\w\s&.]+)", snippet)
            location_match = re.search(r"a\s+([\w\s]+)", snippet)

            results.append({
                "title": title,
                "company": company.group(1).strip() if company else None,
                "location": location_match.group(1).strip() if location_match else location,
                "ral": extract_ral(snippet),
                "link": link
            })

        return results

    except Exception as e:
        print(f"Errore durante la chiamata a Google Custom Search: {e}")
        return []


def extract_ral(text: str):
    """Estrae RAL se trovata nel testo"""
    match = re.search(r"€\s?([\d.,]+)", text)
    if match:
        try:
            return f"{int(match.group(1).replace('.', '').replace(',', '')):,}".replace(",", ".")
        except ValueError:
            return None
    return None


def fetch_salary_benchmark(role: str, location: str):
    """Mock del benchmark retributivo da PayScale (placeholder)"""
    # Potresti in futuro integrare un'API reale qui (PayScale, Glassdoor, etc.)
    return {
        "p50": 52000,
        "p75": 67400,
        "p90": 83000,
        "source": "PayScale/Glassdoor (placeholder)",
        "date": datetime.now().strftime("%Y-%m-%d")
    }


def compute_ranking(jobs, benchmark_p50):
    """Ranking intelligente basato su:
    - RAL più alta → punteggio maggiore
    - Ruoli senior → bonus
    - Vicinanza (se 'remote' o stessa città)
    """
    ranked = []
    for job in jobs:
        score = 50  # base
        ral_val = 0

        # RAL impact
        if job["ral"]:
            try:
                ral_val = int(job["ral"].replace(".", ""))
                ratio = min(ral_val / benchmark_p50, 2.0)
                score += (ratio - 1) * 30
            except ValueError:
                pass

        # Seniority bonus
        if re.search(r"senior|lead|manager|head", job["title"], re.I):
            score += 10

        # Locality bonus
        if job["location"] and ("remote" in job["location"].lower() or "italia" in job["location"].lower()):
            score += 5

        ranked.append({**job, "score": round(min(score, 100), 1)})

    # Ordina per punteggio discendente
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked


# === ROUTES ===

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Pagina iniziale"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": None,
        "benchmark": None
    })


@app.post("/run", response_class=HTMLResponse)
async def run_job_search(
    request: Request,
    title: str = Form(...),
    location: str = Form(...),
    years: int = Form(0)
):
    """Esegue la ricerca del lavoro e mostra i risultati"""
    print(f"🔍 Ricerca: {title} @ {location}, esperienza: {years} anni")

    jobs = fetch_job_listings(title, location)
    benchmark = fetch_salary_benchmark(title, location)

    ranked = compute_ranking(jobs, benchmark["p50"])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": ranked,
        "benchmark": benchmark
    })


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "jobsearch-agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
