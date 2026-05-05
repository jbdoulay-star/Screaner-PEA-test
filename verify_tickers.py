import yfinance as yf
import json
from datetime import datetime

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
    "ASML", "BESI", "PHI1", "SHL", "ADS", "BMW", "VOS", "3WG",
    # ── ETFs PEA ──────────────────────────────────────────
    "EWLD", "RS2K", "PANX", "PUST", "PCEU", "PAEEM", "PASI", "PINE",
    "PTPXE", "EDEF", "FRIDF",

    # ── Construction / Industrie ──────────────────────────
    "DG",       # Vinci
    "EN",       # Bouygues
    "SU",       # Schneider Electric
    "LR",       # Legrand
    "PRY",      # Prysmian
    "NEX",      # Nexans
    "SIE",      # Siemens
    "RXL",      # Rexel
    "SPIE",     # SPIE
    "FGR",      # Eiffage
    "ALO",      # Alstom
    "BVI",      # Bureau Veritas
    "DLTA",     # Delta Plus
    "IPS",      # Ipsos

    # ── Matériaux / Chimie ────────────────────────────────
    "AI",       # Air Liquide
    "BAS",      # BASF
    "SOLB",     # Solvay
    "AKE",      # Arkema
    "UMI",      # Umicore
    "HEIDELBERG", # Heidelberg Materials
    "CRH",      # CRH
    "BZZ",      # Buzzi
    "VCT",      # Vicat
    "VRAL",     # Verallia
    "SGO",      # Saint-Gobain

    # ── Santé / Pharma ────────────────────────────────────
    "SAN",      # Sanofi
    "NOVO",     # Novo Nordisk
    "ERF",      # Eurofins Scientific
    "SHL",      # Sartorius Stedim Biotech
    "UCB",      # UCB
    "IPN",      # Ipsen
    "BIO",      # bioMérieux
    "GRF",      # Grifols
    "RMS",      # Guerbet (approximatif)

    # ── Luxe / Mode ───────────────────────────────────────
    "MC",       # LVMH
    "RMS",      # Hermès
    "OR",       # L'Oréal
    "KER",      # Kering
    "MONC",     # Moncler
    "BRUN",     # Brunello Cucinelli
    "CDI",      # Christian Dior
    "RCO",      # Rémy Cointreau
    "JD",       # JD Sports Fashion
    "ZAL",      # Zalando
    "CATA",     # Catana

    # ── Distribution / Alimentation ───────────────────────
    "AD",       # Ahold Delhaize
    "CA",       # Carrefour
    "JRM",      # Jerónimo Martins
    "COLR",     # Colruyt
    "DAN",      # Danone
    "HEIN",     # Heineken
    "ABI",      # AB InBev
    "CARL",     # Carlsberg
    "RI",       # Pernod Ricard
    "BEIR",     # Beiersdorf

    # ── Energie / Pétrole ─────────────────────────────────
    "TTE",      # TotalEnergies
    "ENI",      # Eni
    "REP",      # Repsol
    "OMV",      # OMV
    "GALP",     # Galp
    "EQNR",     # Equinor
    "NES",      # Neste
    "AKRBP",    # Aker BP
    "RUB",      # Rubis
    "MAU",      # Maurel & Prom
    "FUR",      # Fugro

    # ── Utilities / Energie renouvelable ──────────────────
    "IBE",      # Iberdrola
    "ENEL",     # Enel
    "ENGI",     # Engie
    "RWE",      # RWE
    "ORSTED",   # Ørsted
    "EDP",      # EDP
    "EDPR",     # EDP Renováveis
    "VER",      # Verbund

    # ── Technologie ───────────────────────────────────────
    "ASML",     # ASML
    "SAP",      # SAP
    "STM",      # STMicroelectronics
    "DSY",      # Dassault Systèmes
    "IFX",      # Infineon
    "BESI",     # ASM International / BE Semiconductor
    "ADYEN",    # Adyen
    "AUB",      # Aubay
    "NEUR",     # Neurones
    "ITL",      # IT Link
    "EVS",      # EVS

    # ── Aéronautique / Défense ────────────────────────────
    "AIR",      # Airbus
    "SAF",      # Safran
    "HO",       # Thales
    "AM",       # Dassault Aviation
    "LDO",      # Leonardo
    "RHM",      # Rheinmetall
    "SAAB",     # Saab
    "HAG",      # Hensoldt

    # ── Banques / Assurances / Finance ────────────────────
    "BNP",      # BNP Paribas
    "ACA",      # Crédit Agricole
    "GLE",      # Société Générale
    "CS",       # AXA
    "ALV",      # Allianz
    "MUV2",     # Munich Re
    "G",        # Generali
    "ISP",      # Intesa Sanpaolo
    "SCR",      # SCOR
    "COFA",     # Coface
    "AMUN",     # Amundi
    "VIEL",     # Viel & Cie

    # ── Immobilier ────────────────────────────────────────
    "GFC",      # Gecina
    "ICAD",     # Icade
    "URW",      # Unibail-Rodamco-Westfield
    "LI",       # Klepierre
    "COV",      # Covivio
    "VNA",      # Vonovia
    "LEG",      # LEG Immobilien
    "MRL",      # Merlin Properties
    "CARM",     # Carmila
    "KOF",      # Kaufman & Broad

    # ── Télécommunications ────────────────────────────────
    "ORA",      # Orange
    "DTE",      # Deutsche Telekom
    "TEF",      # Telefónica
    "ILD",      # Iliad
    "PROX",     # Proximus
    "ELISA",    # Elisa
    "TELIA",    # Telia / Telenor
    "TIT",      # Telecom Italia
    "NOS",      # NOS
    "TF1",      # TF1
    "M6",       # M6
    "HCO",      # HighCo
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
