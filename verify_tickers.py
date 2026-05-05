import yfinance as yf
import json
from datetime import datetime

# Liste de base sans suffixes
BASE_TICKERS = [
    # ── CAC 40 / Grandes caps françaises ──────────────────
    "AI", "AIR", "ALO", "CS", "BNP", "EN", "CA", "OR", "MC", "ML",
    "RI", "RNO", "SAF", "SAN", "SGO", "SU", "GLE", "STM", "TTE", "DG",
    "HO", "CAP", "DSY", "ERF", "ENGI", "ELIS",
    # ── Mid-caps françaises ───────────────────────────────
    "ERA", "EL", "ENX", "ETL", "NEX", "GTT", "RMS", "IDL", "NK", "SOI",
    "SPIE", "TE", "THEP", "VK", "VU", "VIR", "UMI", "BLC", "BDU", "4BV",
    "SAP", "RCF", "ALRIB", "FDE", "MEMS", "ALMDG", "ALMDT", "EXENS",
    "EXA", "NOA3", "NAE", "ALAGP",
    # ── Valeurs européennes ───────────────────────────────
    "ASML", "BESI", "PHI1", "SHL", "ADS", "BMW", "1TSLA", "VOS", "3WG",
    # ── ETFs PEA ──────────────────────────────────────────
    "EWLD", "RS2K", "PANX", "PUST", "PCEU", "PAEEM", "PASI", "PINE",
    "PTPXE", "EDEF", "FRIDF",
]

# Priorité des marchés
MARCHES = [".F", ".DE", ".PA"]

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
    # Aucun marché disponible
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
        print(f"✅ {base:12} → {resultat['ticker_retenu']:15} ({resultat['prix']})")
    else:
        print(f"❌ {base:12} → INDISPONIBLE sur .F / .DE / .PA")

# Sauvegarde JSON complète
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
