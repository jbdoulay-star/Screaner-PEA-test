import yfinance as yf
import json
from datetime import datetime

BASE_TICKERS = [
 "MLRIC", "RIC", "ALRIC", "MLDRB", "DRB"
}

# Priorité des marchés pour les valeurs européennes génériques
MARCHES = [".PA", ".DE", ".F", ".BR", ".MC", ".AS", ".LS", ".ST", ".OL", ".HE", ".MI"]

# Dédoublonnage
BASE_TICKERS = list(dict.fromkeys(BASE_TICKERS))


def verifier_ticker(base):
    # Cas 1 : ticker US/direct → pas de suffixe
    if base in TICKERS_DIRECTS:
        try:
            data = yf.Ticker(base)
            prix = data.fast_info.last_price
            if prix and prix > 0:
                return {"base": base, "ticker_retenu": base, "marche": "US", "prix": round(prix, 4), "statut": "OK"}
        except:
            pass
        return {"base": base, "ticker_retenu": None, "marche": None, "prix": None, "statut": "INDISPONIBLE"}

    # Cas 2 : ticker avec marché fixe
    if base in TICKERS_FIXES:
        ticker_complet = base + TICKERS_FIXES[base]
        try:
            data = yf.Ticker(ticker_complet)
            prix = data.fast_info.last_price
            if prix and prix > 0:
                return {"base": base, "ticker_retenu": ticker_complet, "marche": TICKERS_FIXES[base], "prix": round(prix, 4), "statut": "OK"}
        except:
            pass
        return {"base": base, "ticker_retenu": None, "marche": None, "prix": None, "statut": "INDISPONIBLE"}

    # Cas 3 : recherche automatique par suffixe
    for suffixe in MARCHES:
        ticker_complet = base + suffixe
        try:
            data = yf.Ticker(ticker_complet)
            prix = data.fast_info.last_price
            if prix and prix > 0:
                return {"base": base, "ticker_retenu": ticker_complet, "marche": suffixe, "prix": round(prix, 4), "statut": "OK"}
        except:
            continue

    return {"base": base, "ticker_retenu": None, "marche": None, "prix": None, "statut": "INDISPONIBLE"}


# ── Exécution ─────────────────────────────────────────────
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

# ── Sauvegarde JSON ───────────────────────────────────────
with open("verification_tickers.json", "w") as f:
    json.dump({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "resultats": resultats,
        "tickers_retenus": tickers_retenus
    }, f, indent=2, ensure_ascii=False)

# ── Résumé ────────────────────────────────────────────────
ok = sum(1 for r in resultats if r["statut"] == "OK")
ko = sum(1 for r in resultats if r["statut"] == "INDISPONIBLE")

print(f"\n📊 Résumé : {ok} OK / {ko} indisponibles")
print(f"📁 Résultats sauvegardés dans verification_tickers.json")
print(f"\n🎯 Tickers retenus :\n{tickers_retenus}")
