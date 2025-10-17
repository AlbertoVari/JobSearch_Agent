# ---------- utils.py ----------
from datetime import datetime
import math

def estimate_distance_km(location_a, location_b):
    """
    Stima semplice della distanza (fittizia) tra località, 
    utile solo per ranking (non geocoding reale).
    """
    if location_a.lower() == location_b.lower():
        return 0
    elif any(city in location_b.lower() for city in ["milano", "bologna", "torino", "padova"]):
        return 20
    elif any(city in location_b.lower() for city in ["roma", "napoli", "firenze"]):
        return 100
    else:
        return 200


def score_job(job, benchmark):
    """
    Calcola un punteggio (0–100) per ogni annuncio in base a:
    - RAL (vicinanza al benchmark p50–p90)
    - Seniority nel titolo
    - Distanza stimata
    - Presenza di keyword premium
    """
    score = 50  # base

    # --- Retribuzione ---
    salary_posted = job.get("salary_range_posted", "")
    if salary_posted:
        import re
        match = re.search(r'(\d{2,3}[.,]?\d{0,3})', salary_posted)
        if match:
            salary = float(match.group(1).replace(",", "").replace(".", ""))
            p50 = benchmark["p50"]
            p90 = benchmark["p90"]

            if salary >= p90:
                score += 40
            elif salary >= p50:
                score += 25
            elif salary >= 0.8 * p50:
                score += 10
        else:
            score += 0
    else:
        # penalizza se non c'è la RAL
        score -= 5

    # --- Seniority ---
    title = (job.get("title") or "").lower()
    if any(k in title for k in ["senior", "lead", "expert", "head"]):
        score += 15
    elif any(k in title for k in ["junior", "assistant"]):
        score -= 10

    # --- Remote Work ---
    if job.get("remote"):
        score += 5

    # --- Distanza ---
    distance = estimate_distance_km("bologna", job.get("location", ""))
    if distance > 50:
        score -= 5
    elif distance > 100:
        score -= 10

    # --- Premium Skills ---
    premium_skills = ["cloud", "sap", "data", "ai", "python", "kubernetes", "project"]
    if any(skill in title for skill in premium_skills):
        score += 5

    # Clamp 0–100
    return max(0, min(100, score))


def rank_jobs(jobs, benchmark):
    """
    Applica score_job() a tutti gli annunci e restituisce una lista ordinata per punteggio decrescente.
    """
    ranked = []
    for job in jobs:
        s = score_job(job, benchmark)
        ranked.append({
            "apply_url": job.get("apply_url"),
            "score": s,
            "rationale": build_rationale(job, s, benchmark)
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked


def build_rationale(job, score, benchmark):
    """
    Descrizione sintetica della motivazione del punteggio.
    """
    title = job.get("title", "Ruolo")
    salary = job.get("salary_range_posted", "n.d.")
    loc = job.get("location", "")
    p50 = benchmark["p50"]

    if score > 90:
        return f"{title} con RAL molto sopra la mediana ({p50}€) e skill premium."
    elif score > 75:
        return f"{title} con RAL competitiva e località favorevole ({loc})."
    elif score > 60:
        return f"{title} con RAL media e requisiti coerenti con benchmark."
    else:
        return f"{title}: RAL non indicata o inferiore alla mediana ({p50}€)."


# ---------- Optional manual test ----------
if __name__ == "__main__":
    benchmark = {
        "p50": 70000,
        "p75": 85000,
        "p90": 100000
    }
    job = {
        "title": "Senior SAP Project Manager",
        "salary_range_posted": "€85.000 - €95.000",
        "location": "Bologna",
        "remote": True,
        "apply_url": "https://example.com/job"
    }
    print(score_job(job, benchmark))
