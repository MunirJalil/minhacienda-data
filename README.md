# MinHacienda Data — Colombia

A Python CLI tool and data catalog for accessing datasets from the **Ministerio de Hacienda y Crédito Público** (MinHacienda) of Colombia, via the [datos.gov.co](https://www.datos.gov.co) Socrata Open Data API and the [irc.gov.co](https://www.irc.gov.co) investor portal.

## Overview

This project catalogs and provides programmatic access to fiscal and debt data from two sources:

1. **datos.gov.co** (Socrata API) — Budget execution, government income, royalties
2. **irc.gov.co** (Inversión y Reforma Capital) — Public debt profiles, fiscal framework documents, investor presentations

The main minhacienda.gov.co website is protected by Radware bot detection, but both datos.gov.co and irc.gov.co are accessible programmatically.

### Data Coverage

**datos.gov.co (Socrata API — 11 datasets):**
- **Presupuesto General de la Nación (PGN)** — Budget execution, spending, income by fiscal year
- **Sistema General de Regalías (SGR)** — Royalties execution, financial status, cash flow, income
- **Ingresos** — Government revenue by type, disaggregated by year and category
- **Programa Semilleros de la Legalidad** — Social program metrics

**irc.gov.co (Liferay DXP portal — 7 file collections + Power BI):**
- **Perfil de Deuda Bruta GNC** — Monthly Excel snapshots of gross debt profile
- **Histórico Total Deuda GNC** — 93 historical Excel files (time series going back years)
- **Marco Fiscal de Mediano Plazo (MFMP)** — Medium-Term Fiscal Framework PDFs (2015–2024)
- **Plan Financiero** — Financial Plan PDFs (2016–2025)
- **Investor Presentations** — Macro/fiscal outlook decks (2019–2025)
- **CONPES Documents** — Public debt regulations
- **APP Metodologías** — PPP methodology documents and templates
- **Power BI Dashboard** — Interactive public debt profile viewer

### Data Sources

| Source | Platform | Access | Data Type |
|---|---|---|---|
| [datos.gov.co](https://www.datos.gov.co) | Socrata Open Data API | No auth needed | JSON/CSV via REST API |
| [irc.gov.co](https://www.irc.gov.co) | Liferay DXP | Browser-like headers | Excel/PDF file downloads |

- **Provider**: Ministerio de Hacienda y Crédito Público - MinHacienda, Bogotá D.C.
- **API Docs**: [https://dev.socrata.com/docs/queries/](https://dev.socrata.com/docs/queries/)
- **License**: Creative Commons Attribution / Share Alike 4.0 International

## Installation

No dependencies beyond Python 3 standard library:

```bash
git clone https://github.com/MunirJalil/minhacienda-data.git
cd minhacienda-data
```

## Usage — datos.gov.co (Socrata API)

```bash
# List all datasets
python3 fetch_minhacienda.py --list

# Filter by keyword
python3 fetch_minhacienda.py --list --category "Presupuesto"

# Search datasets by keyword
python3 fetch_minhacienda.py --search "ingresos"

# Show dataset metadata
python3 fetch_minhacienda.py --info xjxk-qhsc

# Show column names
python3 fetch_minhacienda.py --columns xjxk-qhsc

# Fetch data (JSON by default)
python3 fetch_minhacienda.py --data xjxk-qhsc --limit 50

# Fetch data as CSV
python3 fetch_minhacienda.py --data xjxk-qhsc --limit 100 --format csv

# Fetch data as formatted table
python3 fetch_minhacienda.py --data xjxk-qhsc --limit 10 --format table

# SoQL query filter
python3 fetch_minhacienda.py --data xjxk-qhsc --query 'vigencia=2026' --limit 50

# Rebuild catalog from API
python3 fetch_minhacienda.py --build-catalog
```

## Usage — irc.gov.co (Investor Portal)

```bash
# List all IRC file collections
python3 fetch_minhacienda.py --irc-list

# Show detailed info for a collection (file names, download URLs)
python3 fetch_minhacienda.py --irc-info irc-deuda-perfil

# Search IRC datasets by keyword
python3 fetch_minhacienda.py --irc-search "deuda"

# Download a file from irc.gov.co
python3 fetch_minhacienda.py --irc-download 'https://www.irc.gov.co/documents/d/guest/perfil-deuda-bruta-gnc-mayo-2026-2?download=true'

# Download to a specific directory
python3 fetch_minhacienda.py --irc-download 'https://www.irc.gov.co/documents/d/guest/perfil-deuda-bruta-gnc-mayo-2026-2?download=true' --output-dir ./data/debt/
```

### IRC Dataset IDs

| ID | Name | Format | Frequency |
|---|---|---|---|
| `irc-deuda-perfil` | Perfil de Deuda Bruta GNC | Excel (.xls) | Monthly |
| `irc-deuda-historico` | Histórico Total Deuda GNC | Excel (.xls) | Monthly (93 files) |
| `irc-mfmp` | Marco Fiscal de Mediano Plazo | PDF | Annual |
| `irc-plan-financiero` | Plan Financiero | PDF | Annual |
| `irc-presentaciones` | Investor Presentations | PDF/PPT | Irregular |
| `irc-conpes` | Normativa Deuda Pública — CONPES | PDF | Irregular |
| `irc-app-metodologias` | APP Metodologías | PDF/Excel | Irregular |

**Note:** irc.gov.co requires browser-like headers (User-Agent, Sec-Fetch-*) for access. The CLI tool handles this automatically. No public REST API exists — all data is file-based.

## Datasets (datos.gov.co)

| ID | Name | Columns | Last Updated |
|---|---|---|---|
| `5phs-yqfw` | Información de Gastos del PGN | 27 | 2026-07-07 |
| `xjxk-qhsc` | Ejecución Presupuestal del PGN | 11 | 2026-07-07 |
| `bpij-5vy9` | Ejecución Presupuestal del PGN (detallada) | 21 | 2026-07-07 |
| `g4qj-2p2e` | Ejecución Presupuestal de Regalías | 11 | 2026-07-14 |
| `si7m-btda` | Programa Semilleros de la Legalidad | 9 | 2023-01-02 |
| `e624-d9uy` | Situación de Caja para Regalías | 15 | 2026-07-14 |
| `br9a-gygu` | Ejecución Financiera de Regalías | 15 | 2026-07-14 |
| `xb6a-jh3a` | Comportamiento de Ingresos Corrientes para Regalías | 13 | 2026-07-14 |
| `22f3-gynv` | Ingresos por Vigencia | 40 | 2026-06-23 |
| `hebe-yxy5` | Ingresos Desagregados Lineal | 67 | 2026-06-23 |
| `34ig-aigy` | Ingresos Desagregados por Vigencia | 75 | 2026-06-23 |

## Project Structure

```
minihacienda-data/
├── fetch_minhacienda.py        # CLI tool (datos.gov.co + irc.gov.co)
├── README.md                   # This file
├── data/
│   ├── datasets_catalog.json   # Full dataset metadata (datos.gov.co)
│   └── irc_catalog.json        # IRC file collection catalog (irc.gov.co)
└── irc-exploration.md          # irc.gov.co portal exploration report
```

## Related Projects

- [banrep-suameca](https://github.com/MunirJalil/banrep-suameca) — Banco de la República (Central Bank) data CLI

## License

Data: Creative Commons Attribution / Share Alike 4.0 International (via datos.gov.co)
Code: MIT