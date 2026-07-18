#!/usr/bin/env python3
"""
MinHacienda Data CLI — Fetch datasets from Colombia's Ministerio de Hacienda y Crédito Público
via the datos.gov.co Socrata API.

Usage:
  python3 fetch_minhacienda.py --list                                    # List all datasets
  python3 fetch_minhacienda.py --list --category "Presupuesto"          # Filter by keyword
  python3 fetch_minhacienda.py --search "ingresos"                       # Search datasets by keyword
  python3 fetch_minhacienda.py --info xjxk-qhsc                          # Dataset metadata
  python3 fetch_minhacienda.py --data xjxk-qhsc --limit 50               # Fetch 50 rows
  python3 fetch_minhacienda.py --data xjxk-qhsc --limit 100 --format csv # CSV output
  python3 fetch_minhacienda.py --data xjxk-qhsc --query 'vigencia=2026'  # SoQL query
  python3 fetch_minhacienda.py --data xjxk-qhsc --limit 10 --format table # Table output
  python3 fetch_minhacienda.py --columns xjxk-qhsc                      # Show column names

Data Source:
  Platform: datos.gov.co (Socrata Open Data API)
  Provider: Ministerio de Hacienda y Crédito Público - MinHacienda, Bogotá D.C.
  API docs: https://dev.socrata.com/docs/queries/

Note:
  The main minhacienda.gov.co site is behind Radware bot protection.
  All data is accessed through the datos.gov.co Socrata API, which is open and
  requires no authentication for public datasets.
"""
import argparse, json, csv, sys, os, urllib.request, urllib.parse
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────

BASE_API = "https://www.datos.gov.co"
CATALOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "datasets_catalog.json")

# ── HTTP helpers ────────────────────────────────────────────────────────────

def fetch_json(url):
    """Fetch JSON from an API endpoint."""
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "MinHacienda-Data-CLI/1.0",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())

def fetch_csv(url):
    """Fetch CSV from an API endpoint."""
    req = urllib.request.Request(url, headers={
        "Accept": "text/csv",
        "User-Agent": "MinHacienda-Data-CLI/1.0",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode()

# ── Catalog ─────────────────────────────────────────────────────────────────

def load_catalog():
    """Load the local dataset catalog."""
    if not os.path.exists(CATALOG_PATH):
        print(f"Error: Catalog file not found at {CATALOG_PATH}", file=sys.stderr)
        print("Run: python3 fetch_minhacienda.py --build-catalog", file=sys.stderr)
        sys.exit(1)
    with open(CATALOG_PATH) as f:
        return json.load(f)

def save_catalog(catalog):
    """Save the dataset catalog."""
    os.makedirs(os.path.dirname(CATALOG_PATH), exist_ok=True)
    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

def build_catalog(dataset_ids):
    """Fetch metadata for all known dataset IDs and build the catalog."""
    catalog = []
    for ds_id in dataset_ids:
        url = f"{BASE_API}/api/views/{ds_id}.json"
        try:
            data = fetch_json(url)
            entry = {
                "id": ds_id,
                "name": data.get("name", ""),
                "description": data.get("description", ""),
                "attribution": data.get("attribution", ""),
                "type": data.get("viewType", ""),
                "category": data.get("category", ""),
                "tags": data.get("tags", []),
                "rowCount": data.get("rowCount"),
                "createdAt": data.get("createdAt"),
                "rowsUpdatedAt": data.get("rowsUpdatedAt"),
                "publicationDate": data.get("publicationDate"),
                "columns": [
                    {
                        "field": c.get("fieldName", ""),
                        "name": c.get("name", ""),
                        "dataType": c.get("dataTypeName", ""),
                        "description": c.get("description", ""),
                    }
                    for c in data.get("columns", [])
                ],
                "apiEndpoint": f"{BASE_API}/resource/{ds_id}.json",
                "csvEndpoint": f"{BASE_API}/api/views/{ds_id}/rows.csv",
                "permalink": f"https://www.datos.gov.co/d/{ds_id}",
            }
            catalog.append(entry)
            print(f"  ✅ {ds_id} → {entry['name'][:60]} ({len(entry['columns'])} cols)")
        except Exception as e:
            print(f"  ❌ {ds_id} → {e}", file=sys.stderr)
    save_catalog(catalog)
    print(f"\nCatalog saved: {CATALOG_PATH} ({len(catalog)} datasets)")
    return catalog

# ── Display ─────────────────────────────────────────────────────────────────

def list_datasets(catalog, category_filter=None):
    """List all datasets, optionally filtered by category keyword."""
    print(f"MinHacienda Data Catalog — {len(catalog)} datasets\n")
    for ds in catalog:
        if category_filter:
            searchable = f"{ds['name']} {ds.get('description','')} {' '.join(ds.get('tags',[]))}".lower()
            if category_filter.lower() not in searchable:
                continue
        cols = ds.get("columns", [])
        print(f"  {ds['id']}")
        print(f"    Name: {ds['name']}")
        print(f"    Description: {ds.get('description', 'N/A')[:120]}")
        print(f"    Columns: {len(cols)}")
        print(f"    Updated: {datetime.fromtimestamp(ds.get('rowsUpdatedAt', 0)).strftime('%Y-%m-%d') if ds.get('rowsUpdatedAt') else 'N/A'}")
        print(f"    URL: {ds.get('permalink', '')}")
        print()

def search_datasets(keyword, catalog=None):
    """Search datasets by keyword in name, description, tags, and column names."""
    if catalog is None:
        catalog = load_catalog()
    kw = keyword.lower()
    results = []
    for ds in catalog:
        searchable_parts = [
            ds.get("name", ""),
            ds.get("description", ""),
            " ".join(ds.get("tags", [])),
        ]
        for c in ds.get("columns", []):
            searchable_parts.append(c.get("name", ""))
            searchable_parts.append(c.get("field", ""))
        searchable = " ".join(searchable_parts).lower()
        if kw in searchable:
            results.append(ds)
    
    if not results:
        print(f"No datasets found matching '{keyword}'")
        return
    
    print(f"Search '{keyword}' — {len(results)} match(es)\n")
    for ds in results:
        print(f"  {ds['id']} → {ds['name']}")
        cols = [c["name"] for c in ds.get("columns", [])]
        if cols:
            matched_cols = [c for c in cols if kw in c.lower()]
            if matched_cols:
                print(f"    Matched columns: {', '.join(matched_cols)}")
        print(f"    URL: {ds.get('permalink', '')}")
        print()

def show_info(ds_id, catalog=None):
    """Show detailed metadata for a single dataset."""
    if catalog is None:
        catalog = load_catalog()
    ds = next((d for d in catalog if d["id"] == ds_id), None)
    if not ds:
        print(f"Dataset '{ds_id}' not found in catalog.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Dataset: {ds['name']}")
    print(f"ID: {ds['id']}")
    print(f"Description: {ds.get('description', 'N/A')}")
    print(f"Attribution: {ds.get('attribution', 'N/A')}")
    print(f"Category: {ds.get('category', 'N/A')}")
    print(f"Tags: {', '.join(ds.get('tags', [])) or 'N/A'}")
    print(f"Rows: {ds.get('rowCount', 'N/A')}")
    updated = ds.get("rowsUpdatedAt")
    if updated:
        print(f"Last Updated: {datetime.fromtimestamp(updated).strftime('%Y-%m-%d %H:%M')}")
    created = ds.get("createdAt")
    if created:
        print(f"Created: {datetime.fromtimestamp(created).strftime('%Y-%m-%d')}")
    print(f"\nColumns ({len(ds.get('columns', []))}):")
    for c in ds.get("columns", []):
        print(f"  - {c['field']} ({c['dataType']}): {c['name']}")
        if c.get("description"):
            print(f"      {c['description'][:120]}")
    print(f"\nEndpoints:")
    print(f"  JSON API:  {ds.get('apiEndpoint', '')}")
    print(f"  CSV:       {ds.get('csvEndpoint', '')}")
    print(f"  Permalink: {ds.get('permalink', '')}")

def show_columns(ds_id, catalog=None):
    """Show column names for a dataset."""
    if catalog is None:
        catalog = load_catalog()
    ds = next((d for d in catalog if d["id"] == ds_id), None)
    if not ds:
        print(f"Dataset '{ds_id}' not found.", file=sys.stderr)
        sys.exit(1)
    print(f"Columns for {ds['name']} ({ds_id}):")
    for i, c in enumerate(ds.get("columns", [])):
        print(f"  {i+1:3d}. {c['name']}  [{c['field']}]  ({c['dataType']})")

# ── Data fetching ───────────────────────────────────────────────────────────

def fetch_data(ds_id, limit=100, query=None, fmt="json"):
    """Fetch data from a dataset via the Socrata API."""
    if query:
        # Use SoQL query endpoint
        url = f"{BASE_API}/resource/{ds_id}.json?{query}&$limit={limit}"
    else:
        url = f"{BASE_API}/resource/{ds_id}.json?$limit={limit}"
    
    if fmt == "csv":
        csv_url = url.replace(".json", ".csv")
        return fetch_csv(csv_url)
    
    return fetch_json(url)

def output_data(data, fmt="json"):
    """Output data in the specified format."""
    if fmt == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif fmt == "csv":
        if isinstance(data, str):
            print(data)
        else:
            print("CSV format requires raw CSV data", file=sys.stderr)
    elif fmt == "table":
        if isinstance(data, list) and data:
            print_table(data)
        elif isinstance(data, str):
            print(data)
        else:
            print("No data to display", file=sys.stderr)
    elif fmt == "count":
        if isinstance(data, list):
            print(f"Rows: {len(data)}")
        else:
            print(f"Data: {data}")

def print_table(rows):
    """Print a list of dicts as a formatted table."""
    if not rows:
        print("No data.")
        return
    
    # Get all column names from first row
    cols = list(rows[0].keys())
    
    # Calculate column widths
    widths = {}
    for c in cols:
        widths[c] = max(len(c), max(len(str(r.get(c, ""))) for r in rows[:50]))
        widths[c] = min(widths[c], 40)  # Cap width
    
    # Print header
    header = " | ".join(c[:widths[c]].ljust(widths[c]) for c in cols[:12])
    print(header)
    print("-" * len(header))
    
    # Print rows
    for r in rows[:50]:
        row_str = " | ".join(str(r.get(c, ""))[:widths[c]].ljust(widths[c]) for c in cols[:12])
        print(row_str)
    
    if len(rows) > 50:
        print(f"\n... {len(rows) - 50} more rows (use --limit to adjust)")

# ── Known dataset IDs ───────────────────────────────────────────────────────

KNOWN_DATASETS = [
    "5phs-yqfw",  # Información de Gastos del PGN
    "xjxk-qhsc",  # Ejecución Presupuestal del PGN
    "bpij-5vy9",  # Ejecución Presupuestal del PGN detallada
    "g4qj-2p2e",  # Ejecución Presupuestal de Regalías
    "si7m-btda",  # Programa Semilleros de la Legalidad
    "e624-d9uy",  # Situación de Caja para Regalías
    "br9a-gygu",  # Ejecución Financiera de Regalías
    "xb6a-jh3a",  # Comportamiento de los Ingresos Corrientes para Regalías
    "22f3-gynv",  # Ingresos por Vigencia
    "hebe-yxy5",  # Ingresos Desagregados Lineal
    "34ig-aigy",  # Ingresos Desagregados por Vigencia
]

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="MinHacienda Data CLI — Fetch datasets from Ministerio de Hacienda (Colombia) via datos.gov.co",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                                    # List all datasets
  %(prog)s --list --category "Presupuesto"            # Filter by keyword
  %(prog)s --search "ingresos"                        # Search by keyword
  %(prog)s --info xjxk-qhsc                           # Dataset metadata
  %(prog)s --data xjxk-qhsc --limit 50                # Fetch 50 rows (JSON)
  %(prog)s --data xjxk-qhsc --limit 100 --format csv   # CSV output
  %(prog)s --data xjxk-qhsc --query 'vigencia=2026'   # SoQL filter
  %(prog)s --columns xjxk-qhsc                        # Show column names
  %(prog)s --build-catalog                             # Rebuild catalog from API
        """,
    )
    parser.add_argument("--list", action="store_true", help="List all datasets")
    parser.add_argument("--category", type=str, default=None, help="Filter list by keyword (e.g., 'Presupuesto')")
    parser.add_argument("--search", type=str, default=None, help="Search datasets by keyword")
    parser.add_argument("--info", type=str, default=None, metavar="DATASET_ID", help="Show dataset metadata")
    parser.add_argument("--data", type=str, default=None, metavar="DATASET_ID", help="Fetch data from a dataset")
    parser.add_argument("--columns", type=str, default=None, metavar="DATASET_ID", help="Show column names")
    parser.add_argument("--limit", type=int, default=100, help="Number of rows to fetch (default: 100)")
    parser.add_argument("--query", type=str, default=None, help="SoQL query string (e.g., 'vigencia=2026')")
    parser.add_argument("--format", type=str, default="json", choices=["json", "csv", "table", "count"], help="Output format (default: json)")
    parser.add_argument("--build-catalog", action="store_true", help="Rebuild the dataset catalog from the API")
    
    args = parser.parse_args()
    
    if args.build_catalog:
        print("Building catalog from datos.gov.co API...")
        build_catalog(KNOWN_DATASETS)
        return
    
    if args.list:
        catalog = load_catalog()
        list_datasets(catalog, args.category)
    elif args.search:
        search_datasets(args.search)
    elif args.info:
        show_info(args.info)
    elif args.columns:
        show_columns(args.columns)
    elif args.data:
        data = fetch_data(args.data, args.limit, args.query, args.format)
        output_data(data, args.format)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()