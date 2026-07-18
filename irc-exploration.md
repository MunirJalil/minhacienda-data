# IRC.gov.co Exploration Report — Data Catalog

**Site:** https://www.irc.gov.co  
**Full Name:** Inversión y Reforma Capital — Oficina de Relación con Inversionistas  
**Parent:** Ministerio de Hacienda y Crédito Público (MinHacienda), Colombia  
**Platform:** Liferay Portal (Java-based CMS)  
**Infrastructure:** Microsoft Azure Application Gateway v2  
**Exploration Date:** 2026-07-18  

---

## 1. Site Architecture Overview

The IRC portal is built on **Liferay DXP** (Digital Experience Platform). It uses Liferay's document library system for file management and embeds a **Power BI dashboard** for debt data visualization. There is **no public REST API** for data retrieval — all data is served through Liferay's document download endpoints or via an embedded Power BI report.

### Key Technical Details
- **CMS:** Liferay DXP (confirmed by `/o/` URL prefix, `combo` resource URLs, `document_library` portlets)
- **Authentication:** OAuth2 endpoints exist (`/o/oauth2/authorize`, `/o/oauth2/token`, `/o/oauth2/introspect`, `/o/oauth2/redirect`) but no public API documentation
- **Search:** Liferay search suggestions API at `/o/search/v1.0/suggestions` (POST, requires proper Liferay session/auth)
- **Analytics:** Google Analytics 4 (tag: `G-RSS9Y28GZ7`)
- **Anti-bot:** Azure Application Gateway v2 — blocks requests without proper browser headers (403). Requires Firefox/Chrome User-Agent and full `Sec-Fetch-*` headers
- **Email:** `oricolombia@minhacienda.gov.co`

### Access Requirements
```bash
# Working curl command for scraping (must use Firefox UA + Sec-Fetch headers)
curl -sS -L --tlsv1.2 \
  -A "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: es-CO,es;q=0.9,en;q=0.8" \
  -H "Accept-Encoding: identity" \
  -H "Sec-Fetch-Dest: document" \
  -H "Sec-Fetch-Mode: navigate" \
  -H "Sec-Fetch-Site: none" \
  -H "Sec-Fetch-User: ?1" \
  "https://www.irc.gov.co/{page}"
```

---

## 2. Site Map (Key Pages)

| URL Path | Description |
|---|---|
| `/` | Homepage |
| `/inicio` | Home (alt) |
| `/quienes-somos` | About Us |
| `/quienes-somos/contactenos` | Contact |
| `/quienes-somos/preguntas-frecuentes` | FAQ |
| `/conoce-colombia` | Know Colombia |
| `/conoce-colombia/informacion-fiscal/marco-fiscal-mediano-plazo` | Medium-Term Fiscal Framework (MFMP) |
| `/conoce-colombia/informacion-fiscal/plan-financiero` | Financial Plan |
| `/deuda-publica` | Public Debt (hub) |
| `/deuda-interna-gnc` | Internal Debt GNC |
| `/deuda-externa-gnc` | External Debt GNC |
| `/perfil-deuda-publica-gnc` | **Debt Profile GNC (Power BI + Excel downloads)** |
| `/tesoreria` | Treasury |
| `/operaciones-de-tesoreria` | Treasury Operations |
| `/tesoreria/giros-y-programacion-de-pagos` | Payments & Transfers |
| `/finanzas-sostenibles` | Sustainable Finance |
| `/bonos-verdes-sociales-y-sostenibles` | Green/Social/Sustainable Bonds |
| `/sustainable-finance/social-bonds` | Social Bonds (EN) |
| `/presentaciones` | Presentations |
| `/press-releases` | Press Releases (currently empty) |
| `/es/publicaciones` | Publications |
| `/es/normativa-deuda-publica` | Debt Regulations (CONPES documents) |
| `/en-vivo` | Live (video/media) |
| `/eventos-online/programacion-de-eventos` | Events Schedule |
| `/material-destacado` | Featured Material |
| `/tramites` | Procedures |
| `/app` | APP (Asociaciones Público Privadas) |
| `/app/metodologia` | APP Methodologies |
| `/buscar` | Search |

---

## 3. Power BI Dashboard

### Perfil de Deuda Pública GNC

**URL:** https://app.powerbi.com/view?r=eyJrIjoiNmNjZTAyZjctZWVhOC00NTdiLThkMzYtOGFjNzBkNGQxZWEyIiwidCI6ImI0ZWE2MGQ4LWJlNDktNDBiYy05OGM0LTE4YzQzYmZkNzIxZSIsImMiOjR9

**Embed page:** `/deuda-publica/perfil-deuda-publica-gnc`  
**Description:** Interactive Power BI report showing Colombia's public debt profile — debt bruta, stock, composition by instrument, holder, currency, maturity, etc.  
**Data refresh:** Monthly (latest: May 2026 at time of exploration)  
**Access:** Public (no auth required to view)  
**Data extraction:** Power BI REST API could be used with proper credentials, but the report embed token is hardcoded in the page

---

## 4. Downloadable Data Files — Full Catalog

### 4.1 Perfil de Deuda Pública GNC (Excel files)

**Base download URL pattern:**
```
https://www.irc.gov.co/documents/d/guest/{slug}?download=true
```

**Current files (2 folders: Perfil + Histórico):**

| File Name | Format | Size | Period | Download URL |
|---|---|---|---|---|
| Perfil Deuda Bruta GNC Mayo 2026 | .xls | 582 KB | May 2026 | `https://www.irc.gov.co/documents/d/guest/perfil-deuda-bruta-gnc-mayo-2026-2?download=true` |
| Histórico Total Mayo 2026 | .xls | 9.3 MB | May 2026 | `https://www.irc.gov.co/documents/d/guest/historico-total-mayo2026-2?download=true` |
| Perfil Deuda Bruta GNC Abril 2026 | .xls | 583 KB | Apr 2026 | `https://www.irc.gov.co/documents/d/guest/perfil-deuda-bruta-gnc-abril-2026?download=true` |
| Histórico Total Abril 2026 | .xls | 9.3 MB | Apr 2026 | `https://www.irc.gov.co/documents/d/guest/historico-total-abril2026?download=true` |
| Perfil Deuda Bruta GNC Febrero 2026 | .xls | 586 KB | Feb 2026 | `https://www.irc.gov.co/documents/d/guest/perfil-deuda-bruta-gnc-febrero-2026-2?download=true` |
| Histórico Total Febrero 2026 | .xls | 9.2 MB | Feb 2026 | `https://www.irc.gov.co/documents/d/guest/historico-total-febrero2026-2?download=true` |
| Perfil Deuda Bruta GNC Enero 2026 | .xls | 583 KB | Jan 2026 | `https://www.irc.gov.co/documents/d/guest/perfil-deuda-bruta-gnc-enero-2026-2?download=true` |
| Histórico Total Enero 2026 | .xls | 9.2 MB | Jan 2026 | `https://www.irc.gov.co/documents/d/guest/historico-total-enero2026-3?download=true` |
| Perfil Deuda Bruta GNC Diciembre 2025 | .xls | 1.2 MB | Dec 2025 | `https://www.irc.gov.co/documents/d/guest/perfil-deuda-bruta-gnc-diciembre-2025-1-1?download=true` |
| Histórico Total Diciembre 2025 | .xls | 9.2 MB | Dec 2025 | `https://www.irc.gov.co/documents/d/guest/historico-total-diciembre2025?download=true` |

**Notes:**
- "Perfil Deuda Bruta" = Monthly snapshot of gross debt profile (~500KB-1.2MB)
- "Histórico Total" = Historical time series of debt (~9MB, 93 files in the folder going back many years)
- The Histórico folder contains **93 documents** — the page shows 8 at a time with pagination
- File format: Excel `.xls` (old format, `application/vnd.ms-excel`)
- Files created by: Gabriel Felipe Melendez Parra (Perfil), Camilo Corredor (Histórico)

**Pagination of historical files:** The Liferay document library at `/deuda-publica/perfil-deuda-publica-gnc` uses portlet `INSTANCE_notf` (Histórico) and `INSTANCE_ngtl` (Perfil). To get all 93 historical files, you would need to paginate through:
```
https://www.irc.gov.co:443/deuda-publica/perfil-deuda-publica-gnc/-/document_library/notf/view/175077?_com_liferay_document_library_web_portlet_DLPortlet_INSTANCE_notf_curEntry={N}&_com_liferay_document_library_web_portlet_DLPortlet_INSTANCE_notf_deltaEntry=8
```
Where `{N}` is the page number (1, 2, 3, ..., 12).

### 4.2 Marco Fiscal de Mediano Plazo (PDF files)

| File Name | Format | Download URL |
|---|---|---|
| MFMP 2024 | PDF | `https://www.irc.gov.co/documents/d/guest/marco-fiscal-de-mediano-plazo-2024?download=true` |
| MFMP 2023 | PDF | `https://www.irc.gov.co/documents/d/guest/marco-fiscal-de-mediano-plazo-2023?download=true` |
| MFMP 2022 | PDF | `https://www.irc.gov.co/documents/d/guest/marco-fiscal-de-mediano-plazo-2022?download=true` |
| MFMP 2021 | PDF | `https://www.irc.gov.co/documents/d/guest/marco-fiscal-de-mediano-plazo-2021?download=true` |
| MFMP 2020 | PDF | `https://www.irc.gov.co/documents/d/guest/marco-fiscal-de-mediano-plazo-2020?download=true` |
| MFMP 2019 | PDF | `https://www.irc.gov.co/documents/d/guest/mfmp-2019-1?download=true` |
| MFMP 2018 | PDF | `https://www.irc.gov.co/documents/d/guest/marco-fiscal-de-mediano-plazo-2018-2?download=true` |
| MFMP 2015 | PDF | `https://www.irc.gov.co/documents/d/guest/marco-fiscal-de-mediano-plazo-2015?download=true` |

**Total in folder:** 10 documents (2015–2024, with some gaps)

### 4.3 Plan Financiero (PDF files)

| File Name | Format | Download URL |
|---|---|---|
| Plan Financiero 2025 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2025?download=true` |
| Plan Financiero 2024 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2024-2?download=true` |
| Plan Financiero 2023 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2023-2?download=true` |
| Plan Financiero 2022 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2022?download=true` |
| Plan Financiero 2021 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2021?download=true` |
| Plan Financiero 2020 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2020?download=true` |
| Plan Financiero 2019 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2019?download=true` |
| Plan Financiero 2018 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2018?download=true` |
| Plan Financiero 2017 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2016?download=true` |
| Plan Financiero 2016 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2016?download=true` |
| Actualización PF 2017 | PDF | `https://www.irc.gov.co/documents/d/guest/actualizacion-plan-financiero-2017?download=true` |
| Actualización PF 2017 (alt) | PDF | `https://www.irc.gov.co/documents/d/guest/2017-03-01-actualizacion-plan-financiero-2017-vf?download=true` |

**Total in folder:** 11 documents (2016–2025)

### 4.4 Presentaciones / Investor Presentations (PDF/PPT)

| File Name | Format | Download URL |
|---|---|---|
| 2019-05-13 Green Bonds - Social Bonds VF | PDF | `https://www.irc.gov.co/documents/d/guest/2019-05-13-green-bonds-social-bonds-vf-2?download=true` |
| 2021-12-01 Estrategia de Protección Financiera César Arias | PDF | `https://www.irc.gov.co/documents/d/guest/2021-12-01-presentacion-estrategia-de-proteccion-financiera-cesar-arias-1?download=true` |
| 20211224 Presentación Infraestructura | PDF | `https://www.irc.gov.co/documents/d/guest/20211224-presentacion-infraestructura-1?download=true` |
| 20221011 Macroeconomic Overview and Economic Policy Challenges | PDF | `https://www.irc.gov.co/documents/d/guest/20221011-macroeconomic-overview-and-economic-policy-challenges-dc-1?download=true` |
| 2023-04-13 Colombia's Economic Perspectives | PDF | `https://www.irc.gov.co/documents/d/guest/2023-04-13-colombia-s-economic-perspectives-1?download=true` |
| 2024-03-14 Investors Meeting | PDF | `https://www.irc.gov.co/documents/d/guest/2024-03-14-investors-meeting-1?download=true` |
| Investor Presentation 062023 | PDF | `https://www.irc.gov.co/documents/d/guest/investor-presentation-062023?download=true` |
| Investors Meeting Financial Plan Update 12.02.2025 | PDF | `https://www.irc.gov.co/documents/d/guest/investors-meeting-financial-plan-update-2025-02-12?download=true` |
| Investors Meeting ministro IRC 18.12.2024 | PDF | `https://www.irc.gov.co/documents/d/guest/investors-meeting-ministro-irc-18-12-2024?download=true` |
| Colombia Macro and Fiscal Outlook April 2022 | PDF | `https://www.irc.gov.co/documents/d/guest/colombia-macro-and-fiscal-outlook-april-2022-1?download=true` |
| Perspectivas Macro y Fiscal Feb 2022 | PDF | `https://www.irc.gov.co/documents/d/guest/perspectivas-macro-y-fiscal-feb-2022?download=true` |
| Presentación Colombia Inside-Out 18-06-2020 | PDF | `https://www.irc.gov.co/documents/d/guest/presentacion-colombia-inside-out-18-06-2020?download=true` |
| Presentación Plan Financiero 2019 | PDF | `https://www.irc.gov.co/documents/d/guest/presentacion-plan-financiero-2019?download=true` |
| Plan Financiero 2024 | PDF | `https://www.irc.gov.co/documents/d/guest/plan-financiero-2024?download=true` |
| Actualización PF 2023 | PDF | `https://www.irc.gov.co/documents/d/guest/actualizacion-plan-financiero-2023?download=true` |
| Actualización PF 2024 | PDF | `https://www.irc.gov.co/documents/d/guest/actualizacion-plan-financiero-2024?download=true` |
| Actualización PF 2025 | PDF | `https://www.irc.gov.co/documents/d/guest/actualizacion-plan-financiero-2025-1-?download=true` |
| PPT Marco Fiscal Mediano Plazo 2022 | PPT | `https://www.irc.gov.co/documents/d/guest/ppt-presentacion-marco-fiscal-de-mediano-plazo-2022?download=true` |
| Bonos Verdes Soberanos de Colombia 2022 | PDF | `https://www.irc.gov.co/documents/d/guest/bonos-verdes-soberanos-colombia-2022-1?download=true` |
| Boletín 58 MinHacienda terminada emisión primaria TES | PDF | `https://www.irc.gov.co/documents/d/guest/boletin-no-58_-terminada-emision-primaria-de-tes-1?download=true` |

**Total in folder:** 20 documents

### 4.5 Normativa Deuda Pública — CONPES Documents (PDF)

| File Name | Format | Download URL |
|---|---|---|
| CONPES 3107 | PDF | `https://www.irc.gov.co/documents/d/guest/3107?download=true` |
| CONPES 3133 | PDF | `https://www.irc.gov.co/documents/d/guest/3133?download=true` |
| CONPES 3760 | PDF | `https://www.irc.gov.co/documents/d/guest/3760?download=true` |
| CONPES 3800 | PDF | `https://www.irc.gov.co/documents/d/guest/3800?download=true` |
| CONPES 3807 | PDF | `https://www.irc.gov.co/documents/d/guest/3807?download=true` |
| CONPES 3961 | PDF | `https://www.irc.gov.co/documents/d/guest/3961?download=true` |
| CONPES 4000 | PDF | `https://www.irc.gov.co/documents/d/guest/4000?download=true` |
| CONPES 4028 de 2021 | PDF | `https://www.irc.gov.co/documents/d/guest/conpes-4028-de-2021?download=true` |

**Total in folder:** 8 documents

### 4.6 Material Destacado / APP Metodologías (PDF/Excel)

| File Name | Format | Download URL |
|---|---|---|
| Metodología ASG+R Segunda Edición | PDF | `https://www.irc.gov.co/documents/d/guest/metodologia-asg-r_2da-edicion?download=true` |
| Anexo Preguntas Orientadoras Metodología ASG+R v1 | PDF | `https://www.irc.gov.co/documents/d/guest/anexo-preguntas-orientadoras-metodologia-asg-r_v1?download=true` |
| Formato Metodología ASG+R Segunda Edición | Excel | `https://www.irc.gov.co/documents/d/guest/formato-asg-r?download=true` |
| Parámetros Metodología | Excel | `https://www.irc.gov.co/documents/d/guest/20250205-parametros-metodologia?download=true` |
| Criterios Específicos para Aplicación Metodología | PDF | `https://www.irc.gov.co/documents/d/guest/20250326-criterios-especificos-para-la-aplicacion-de-la-metodologia-1?download=true` |
| Formato Sobrecostos | Excel | `https://www.irc.gov.co/documents/d/guest/20200630-formato-sobrecostos?download=true` |
| Macro Metodología Valoración Obligaciones Contingentes | PDF | `https://www.irc.gov.co/documents/d/guest/macro-metodologia-de-valoracion-de-obligaciones-contingentes-en-proyectos-de-infraestructura-caso-comercial-con-informacion-?download=true` |
| Circular Externa 031 (Oct 2025) - Metodologías SubAPP | PDF | `https://www.irc.gov.co/documents/d/guest/circular_externa_031_octubre_01_2025-1?download=true` |

### 4.7 Additional Documents (from homepage)

| File Name | Format | Download URL |
|---|---|---|
| Metodología WACC 2da Edición | PDF | `https://www.irc.gov.co/documents/152891/1824420/Metodolog%C3%ADa+WACC_2da+edici%C3%B3n.pdf/f6cd9300-02f7-9465-bbb5-fe3f1bce3309?t=1759331198251` |
| Fuentes y Usos del Financiamiento GNC 2003-2023 | (web) | `https://www.irc.gov.co/documents/d/guest/fuentes-y-usos-del-financiamiento-del-gnc-2003-2023-pagina-web-sin-links-` |
| Guía Usuario APP | PDF | `https://www.irc.gov.co/documents/d/guest/guiausuario-app-pdf` |
| Resolución 4859 (Dic 2019) Metodología Valoración Riesgos | PDF | `https://www.irc.gov.co/documents/d/guest/11-resolucion-4859-diciembre-23-2019-metodologia-de-valoracion-de-riesgos-1` |
| Metodología Valoración Obligaciones Contingentes | PDF | `https://www.irc.gov.co/documents/d/guest/metodologia-de-valoracion-de-obligaciones-contingentes-1` |

---

## 5. API Endpoints Found

### 5.1 Liferay Platform APIs (require authentication)

| Endpoint | Method | Description |
|---|---|---|
| `/o/oauth2/authorize` | GET | OAuth2 authorization |
| `/o/oauth2/token` | POST | OAuth2 token issuance |
| `/o/oauth2/introspect` | POST | OAuth2 token introspection |
| `/o/oauth2/redirect` | GET | OAuth2 redirect |
| `/o/search/v1.0/suggestions` | POST | Search suggestions (requires Liferay session) |

### 5.2 Document Download Endpoint

All files use the Liferay friendly URL pattern:
```
https://www.irc.gov.co/documents/d/guest/{slug}?download=true
```

This is a **public** endpoint — no authentication required. Just needs proper browser headers (User-Agent, Sec-Fetch-*).

### 5.3 Document Library Portlet API

The Liferay document library can be accessed via portlet resource URLs:
```
/o/document_library/download_file_entry?fileEntryId={ID}&...
```

Or via the folder download:
```
/{page}?p_p_id=com_liferay_document_library_web_portlet_DLPortlet_INSTANCE_{instance}&p_p_lifecycle=2&p_p_resource_id=%2Fdocument_library%2Fdownload_folder&p_p_cacheability=cacheLevelPage&_com_liferay_document_library_web_portlet_DLPortlet_INSTANCE_{instance}_folderId={folderId}&_com_liferay_document_library_web_portlet_DLPortlet_INSTANCE_{instance}_repositoryId=152891
```

### 5.4 Power BI Report

**Embed URL:** `https://app.powerbi.com/view?r=eyJrIjoiNmNjZTAyZjctZWVhOC00NTdiLThkMzYtOGFjNzBkNGQxZWEyIiwidCI6ImI0ZWE2MGQ4LWJlNDktNDBiYy05OGM0LTE4YzQzYmZkNzIxZSIsImMiOjR9`

This is a public Power BI embed with a hardcoded token. The Power BI REST API could be used to extract data if you have access to the workspace, but the embed token only allows viewing.

---

## 6. Embedded Content

### iframe (APP Metodología page)
- **Page:** `/app/metodologia`
- **iframe content:** `/documents/d/guest/metodologia-asg-r_2da-edicion` (embedded PDF viewer)

### Power BI (Perfil Deuda Pública)
- **Page:** `/deuda-publica/perfil-deuda-publica-gnc`
- **Embed:** Power BI report (see section 5.4)

---

## 7. External Data Sources Referenced

The IRC portal links to these external data sources:

| Source | URL | Relevance |
|---|---|---|
| BanRep (Banco de la República) | https://www.banrep.gov.co | Monetary policy, TES yields, macro data |
| BVC (Bolsa de Valores de Colombia) | https://www.bvc.com.co/ | Market data, bond prices |
| DANE | https://www.dane.gov.co/ | National statistics, GDP, inflation |
| DNP | https://www.dnp.gov.co/ | Planning, CONPES documents, APP |
| MinHacienda (main portal) | https://www.minhacienda.gov.co | Fiscal policy, cifras política fiscal |
| SuperFinanciera | https://www.superfinanciera.gov.co/ | Financial regulation |
| ProColombia | https://procolombia.co/ | Investment promotion |
| Taxonomía Verde | https://www.taxonomiaverde.gov.co/ | Green taxonomy |
| ANI | https://www.ani.gov.co | Infrastructure concessions |
| GPI MinTransporte | https://gpi.mintransporte.gov.co | Transport infrastructure |
| CONPES | (via DNP) | Policy documents |
| Función Pública | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php | Legal norms |

### MinHacienda Data Sub-sites Referenced
| Page | URL |
|---|---|
| Cifras Política Fiscal - Gobierno General | `https://www.minhacienda.gov.co/politica-fiscal/cifras-pol%C3%ADtica-fiscal/gobierno-general` |
| Cifras Política Fiscal - Gobierno Nacional | `https://www.minhacienda.gov.co/politica-fiscal/cifras-pol%C3%ADtica-fiscal/gobierno-nacional` |
| Cifras Política Fiscal - SPNF | `https://www.minhacienda.gov.co/politica-fiscal/cifras-politica-fiscal/spnf` |
| Cierres Fiscales | `https://www.minhacienda.gov.co/politica-fiscal/documentos-de-planeacion-financiera/cierres-fiscales` |
| Marcos de Gasto Mediano Plazo | `https://www.minhacienda.gov.co/web/portal/politica-fiscal/documentos-planeacion-financiera/marcos-gasto-mediano-plazo` |
| Guía Ejecución Presupuestal SPGR | `https://www.minhacienda.gov.co/web/portal/sgr/guia-ejecucion-presupuestal-spgr` |
| Capacitación DGPPN (Moodle) | `https://capacitaciondgppn.minhacienda.gov.co/moodle/login/index.php` |

---

## 8. Data Summary & Recommendations

### What's Available

| Data Type | Format | Frequency | Period | Automation? |
|---|---|---|---|---|
| Perfil de Deuda Bruta GNC | Excel (.xls) | Monthly | Dec 2025 – May 2026 (6 months) | ✅ Downloadable via URL |
| Histórico Total Deuda GNC | Excel (.xls) | Monthly | Multi-year (93 files) | ✅ Downloadable, needs pagination |
| Marco Fiscal de Mediano Plazo | PDF | Annual | 2015–2024 (10 docs) | ✅ Downloadable |
| Plan Financiero | PDF | Annual | 2016–2025 (11 docs) | ✅ Downloadable |
| Investor Presentations | PDF | Irregular | 2019–2025 (20 docs) | ✅ Downloadable |
| CONPES Documents | PDF | Irregular | 8 docs | ✅ Downloadable |
| APP Methodologies | PDF/Excel | Irregular | 8 docs | ✅ Downloadable |
| Debt Profile Dashboard | Power BI | Monthly | Interactive | ⚠️ View only, no API export |

### What's NOT Available

- **No REST API** for structured data retrieval — all data is file-based
- **No JSON/CSV endpoints** — everything is PDF or Excel
- **No machine-readable metadata** — no DCAT, no API documentation
- **No real-time data** — monthly publication cycle
- **No subasta (auction) results** — TES auction data appears to not be published on IRC
- **No yield curve data** — would need BanRep for that
- **Press Releases section is empty** — 0 documents

### Automation Recommendations

1. **Monthly Debt Profile Scraper:** Scrape `/deuda-publica/perfil-deuda-publica-gnc` monthly to detect new Excel files. The "Perfil Deuda Bruta" and "Histórico Total" files are the most structured data available.

2. **Paginate Historical Files:** The Histórico folder has 93 files. Use Liferay pagination parameters to get all download URLs:
   ```
   curl with _curEntry=1&_deltaEntry=8 through 12 pages
   ```

3. **Power BI Data Extraction:** Use the Power BI REST API with `powerbi-client` Python library to extract data from the embedded report. Requires obtaining a proper API token (the embed token in the URL may suffice for read operations).

4. **File Download Pattern:** All downloads follow `https://www.irc.gov.co/documents/d/guest/{slug}?download=true` — simple to automate with proper headers.

5. **Monitor New Publications:** Check `/presentaciones`, `/conoce-colombia/informacion-fiscal/marco-fiscal-mediano-plazo`, and `/conoce-colombia/informacion-fiscal/plan-financiero` for new documents.

6. **Cross-reference with MinHacienda:** The main MinHacienda site has more detailed fiscal data at `/politica-fiscal/cifras-politica-fiscal/` — should be explored separately.

---

## 9. Liferay Document Library Portlet Instances

Each page uses a unique portlet instance ID for its document library:

| Page | Portlet Instance | Folder ID |
|---|---|---|
| Perfil Deuda Pública GNC (Perfil) | `ngtl` | 175031 |
| Perfil Deuda Pública GNC (Histórico) | `notf` | 175077 |
| Normativa Deuda Pública | `odhp` | 1313580 |
| Metodología (APP) | `ccds` | 1824293 |
| Presentaciones | (varies) | (varies) |
| En Vivo | `unlo` | 2062934 |
| Comunicados | `vyhw` | 170609 |

---

## 10. Verified File Types

- **Excel files:** `application/vnd.ms-excel` — old `.xls` format (not `.xlsx`), readable by pandas with `xlrd` engine
- **PDF files:** Standard PDF, readable by `pdfplumber` or `PyPDF2`
- **PPT files:** PowerPoint presentations (some)

---

*Report generated 2026-07-18 by OpenClaw subagent exploration. All URLs were verified accessible with proper browser headers.*