# MinHacienda Data — Colombia

A Python CLI tool and data catalog for accessing datasets from the **Ministerio de Hacienda y Crédito Público** (MinHacienda) of Colombia, via the [datos.gov.co](https://www.datos.gov.co) Socrata Open Data API.

## Overview

This project catalogs and provides programmatic access to all MinHacienda datasets published on Colombia's open data portal (datos.gov.co). The main minhacienda.gov.co website is protected by Radware bot detection, but the government's open data platform provides clean, API-accessible datasets.

### Data Coverage

- **Presupuesto General de la Nación (PGN)** — Budget execution, spending, income by fiscal year
- **Sistema General de Regalías (SGR)** — Royalties execution, financial status, cash flow, income
- **Ingresos** — Government revenue by type, disaggregated by year and category
- **Programa Semilleros de la Legalidad** — Social program metrics

### Data Source

- **Platform**: [datos.gov.co](https://www.datos.gov.co) — Socrata Open Data API
- **Provider**: Ministerio de Hacienda y Crédito Público - MinHacienda, Bogotá D.C.
- **API Docs**: [https://dev.socrata.com/docs/queries/](https://dev.socrata.com/docs/queries/)
- **License**: Creative Commons Attribution / Share Alike 4.0 International

## Installation

No dependencies beyond Python 3 standard library:

```bash
git clone https://github.com/muanjaba/minhacienda-data.git
cd minhacienda-data
```

## Usage

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

## Datasets

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
├── fetch_minhacienda.py        # CLI tool
├── README.md                   # This file
├── data/
│   └── datasets_catalog.json   # Full dataset metadata catalog
└── irc-exploration.md          # irc.gov.co portal findings (if available)
```

## Related Projects

- [banrep-suameca](https://github.com/muanjaba/banrep-suameca) — Banco de la República (Central Bank) data CLI

## License

Data: Creative Commons Attribution / Share Alike 4.0 International (via datos.gov.co)
Code: MIT