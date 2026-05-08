import yfinance as yf
import json
from datetime import datetime

BASE_TICKERS = [
    # ── Magnificent Seven ─────────────────────────────────
    "AAPL",     # Apple (NASDAQ direct, pas besoin de suffixe)
    "MSFT",     # Microsoft
    "GOOGL",    # Alphabet
    "AMZN",     # Amazon
    "NVDA",     # Nvidia
    "META",     # Meta
    "TSLA",     # Tesla

    # ── Valeurs européennes & autres ──────────────────────
    "DG",       # Vinci
    "VU",       # Vusion Group
    "VLV",      # Volvo (Stockholm)
    "QURE",     # Unicure (NASDAQ direct)
    "TTE",      # TotalEnergies
    "THEP",     # Thermador
    "HO",       # Thales
    "TEP",      # Teleperformance
    "TE",       # Technip Energies
    "STM",      # ST Microelectronics
    "STLAM",    # Stellantis (Milan)
    "SOLB",     # Solvay (Bruxelles)
    "SOI",      # Soitec
    "GLE",      # Société Générale
    "SIE",      # Siemens AG
    "ENR",      # Siemens Energy
    "SU",       # Schneider Electric
    "SAN",      # Sanofi
    "RNO",      # Renault
    "QUBT",     # Quantum Computing (NASDAQ direct)
    "PHIA",     # Philips (Amsterdam)
    "RI",       # Pernod Ricard
    "HSCE",     # PEAHSCEI China ETF (Hong Kong)
    "PARRO",    # Parrot SA
    "PXT",      # Parex Resources (Toronto)
    "ORA",      # Orange
    "NDX1",     # Nordex
    "NEL",      # NEL ASA (Oslo)
    "MEMS",     # MEMSCAP
    "ALMDT",    # Median Technologies
    "IDL",      # ID Logistics
    "FLOW",     # Flow Traders (Amsterdam)
    "RACE",     # Ferrari (Milan)
    "ALEXA",    # Exxail Technologies
    "ETL",      # Eutelsat
    "EL",       # Essilor Luxottica
    "ERA",      # Eramet
    "ENGI",     # Engie
    "ELIS",     # Elis
    "DRO",      # DroneShield (ASX — à vérifier séparément)
    "MLRIC",    # de Richebourg
    "DELL",     # Dell Technologies (NYSE direct)
    "DSY",      # Dassault Systèmes
    "ACA",      # Crédit Agricole
    "SGO",      # Saint-Gobain
    "CMG",      # Chipotle (NYSE direct)
    "CAT",      # Caterpillar (NYSE direct)
    "CAP",      # Capgemini
    "BVI",      # Bureau Veritas
    "AVGO",     # Broadcom (NASDAQ direct)
    "EN",       # Bouygues
    "BNP",      # BNP Paribas
    "BESI",     # BE Semiconductors (Amsterdam)
    "CS",       # AXA
    "ASML",     # ASML (Amsterdam)
    "ALO",      # Alstom
    "AIR",      # Airbus
    "AI",       # Air Liquide
    "AF",       # Air France KLM
    "ADBE",     # Adobe (NASDAQ direct)
    "ADS",      # Adidas
]

# Tickers US/hors Europe à traiter directement (sans suffixe)
TICKERS_DIRECTS = {
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
    "QURE", "QUBT", "DELL", "CMG", "CAT", "AVGO", "ADBE"
}

# Tickers avec marché fixe (ne pas tester plusieurs suffixes)
TICKERS_FIXES = {
    "SOLB":  ".BR",   # Solvay → Bruxelles
    "PHIA":  ".AS",   # Philips → Amsterdam
    "FLOW":  ".AS",   # Flow Traders → Amsterdam
    "BESI":  ".AS",   # BE Semiconductors → Amsterdam
    "ASML":  ".AS",   # ASML → Amsterdam
    "RACE":  ".MI",   # Ferrari → Milan
    "STLAM": ".MI",   # Stellantis → Milan
    "NDX1":  ".DE",   # Nordex → Xetra
    "ENR":   ".DE",   # Siemens Energy → Xetra
    "SIE":   ".DE",   # Siemens AG → Xetra
    "ADS":   ".DE",   # Adidas → Xetra
    "VLV":   ".ST",   # Volvo → Stockholm
    "NEL":   ".OL",   # NEL ASA → Oslo
    "PXT":   ".TO",   # Parex → Toronto
    "DRO":   ".AX",   # DroneShield → ASX
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
