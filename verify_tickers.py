import yfinance as yf
import json
from datetime import datetime

BASE_TICKERS = [
    # ── Magnificient seven ────────────────────────────────
    "APC", "MSF", "ABE", "AMZ", "NVD", "FB2A", "TL0",
    # ── Nouvelles ────────────────────────────────
    "DBG",
    
]

# Dédoublonnage
BASE_TICKERS = list(dict.fromkeys(BASE_TICKERS))

# Priorité des marchés
MARCHES = [".PA", ".DE", ".F", ".BR", ".MC", ".AS", ".LS", ".ST", ".OL", ".HE"]

def verifier_ticker(base):
    for suffixe in MARCHES:
        ticker_complet = base + suffixe
        try:
            data = yf.Ticker(ticker_complet)
            prix = data.fast_info.last_price
            if prix and prix > 0:
                return {
                    "base": base,
                    "ticker_retenu": ticker_complet,
                    "marche": suffixe,
                    "prix": round(prix, 4),
                    "statut": "OK"
                }
        except:
            continue
    return {
        "base": base,
        "ticker_retenu": None,
        "marche": None,
        "prix": None,
        "statut": "INDISPONIBLE"
    }

resultats = []
tickers_retenus = []

print("🔍 Vérification en cours...\n")

for base in BASE_TICKERS:
    resultat = verifier_ticker(base)
    resultats.append(resultat)

    if resultat["statut"] == "OK":
        tickers_retenus.append(resultat["ticker_retenu"])
        print(f"✅ {base:15} → {resultat['ticker_retenu']:18} ({resultat['prix']})")
    else:
        print(f"❌ {base:15} → INDISPONIBLE")

# Sauvegarde JSON
with open("verification_tickers.json", "w") as f:
    json.dump({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "resultats": resultats,
        "tickers_retenus": tickers_retenus
    }, f, indent=2, ensure_ascii=False)

# Résumé
ok = sum(1 for r in resultats if r["statut"] == "OK")
ko = sum(1 for r in resultats if r["statut"] == "INDISPONIBLE")

print(f"\n📊 Résumé : {ok} OK / {ko} indisponibles")
print(f"📁 Résultats sauvegardés dans verification_tickers.json")
print(f"\n🎯 Tickers retenus :\n{tickers_retenus}")
