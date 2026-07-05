# 🛡️ IDBI Bank MSME Alternate Credit Intelligence Hub
### A Unified Lending Interface (ULI) & Account Aggregator (AA) Multi-Agent Processing Pipeline Engine

An advanced alternate-data credit underwriting and risk assessment engine built for the modern Indian Digital Public Infrastructure (DPI) landscape. The system ingests asynchronous data payloads from the **Unified Lending Interface (ULI)** (GSTN, NPCI/UPI, EPFO) and **Account Aggregator (AA)** networks, orchestrates decentralized processing via deterministic domain-expert agents, computes a 4-pillar credit score out of 1000 points, and instantly maps loan terms into compliance-ready **Open Credit Network (OCEN)** payload schemas.

---

## 🏗️ System Architecture & Data Flow

The platform decouples data acquisition from statistical processing and language generation, ensuring sub-second evaluation times and zero structural/mathematical hallucination risk.

1. **Plumbing Layer** (`services/`) — Simulated API sandboxes for ULI data nodes (GST, UPI, EPFO) and consented AA financial data networks.
2. **Domain Expert Agents Layer** (`agents/`) — Deterministic algorithmic modules that isolate risk signals, running mathematical calculations asynchronously over raw JSON arrays.
3. **Orchestration & Scoring Engine** (`scoring_agent.py`) — Consolidates isolated domain vectors into a 4-pillar risk scorecard and invokes a Groq-hosted LLM to compile an institutional Credit Underwriting Memo.
4. **Ecosystem Exit Node** (`ocen_service.py`) — Evaluates parameters against credit risk bands to issue loan limits and fixed APR interest rates, structured into valid OCEN transactional payloads.
5. **Interactive Operations Hub** (`app/`) — A Streamlit dashboard visualizing risk matrix radar charts and system log telemetry.

```
ULI / AA Data Sources
        │
        ▼
  Plumbing Layer (services/)
        │
        ▼
  Domain Expert Agents (agents/) ── GST, UPI, EPFO, AA
        │
        ▼
  Scoring & Orchestration Engine ── 4-Pillar Score + LLM Memo
        │
        ▼
  OCEN Ecosystem Exit Node ── Loan Limit / APR / Payload
        │
        ▼
  Streamlit Dashboard (app/)
```

---

## 📊 Core Underwriting Pillars (1000-Point Matrix)

The deterministic scoring algorithm evaluates businesses across four isolated credit dimensions:

| Underwriting Pillar | Max Weight | Core Tracked Metrics & Risk Signals |
| :--- | :---: | :--- |
| **Revenue & Scale Stability** | 300 pts | GST vintage (months), MoM turnover growth trends, B2B vendor concentration risk |
| **Cash Flow Consistency** | 350 pts | 90-day merchant UPI volumes, transactional velocity vectors, Average Daily Balance (ADB) |
| **Operational Formality** | 150 pts | EPFO infrastructure validation, formal employee count, headcount stability |
| **Transaction Maturity** | 200 pts | GSTR-3B filing punctuality, cheque bounces, recurring ECS mandate failures |

**Total: 1000 points**, mapped to risk bands (Approved / Conditional / Critical Risk) that drive the final OCEN loan decision.

---

## 📁 Repository Structure

```text
idbi-msme-underwriter/
├── app/
│   └── streamlit_dashboard.py      # Interactive UI dashboard & radar visualization
├── agents/
│   ├── __init__.py
│   ├── base_agent.py               # Shared Pydantic structural state models
│   ├── gst_agent.py                # Tax compliance & turnover metrics
│   ├── upi_agent.py                # Digital merchant cash flow velocity
│   ├── epfo_agent.py               # Headcount & workforce indicators
│   ├── aa_agent.py                 # Bank statement risk triggers
│   └── scoring_agent.py            # Aggregates scores & compiles LLM Underwriting Memo
├── services/
│   ├── __init__.py
│   ├── uli_service.py              # Simulated ULI API data pipelines
│   ├── aa_service.py               # Account Aggregator consent & telemetry
│   └── ocen_service.py             # Encapsulates loan terms into OCEN-ready schemas
├── data/
│   ├── mock_personas/              # 105 synthetic MSME profiles
│   └── synthetic_generator.py      # Procedural data generation script
├── requirements.txt                # Dependency manifest
├── .gitignore                      # Excludes secrets (.env, etc.)
└── README.md                       # Project documentation
```

---

## 🛠️ Quickstart & Local Installation

### 1. Clone & Install Dependencies

```bash
# Upgrade core installer tools
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Secrets

Create a `.env` file in the project root and add your Groq API credentials (already excluded from version control via `.gitignore`):

```
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

> **Note:** If no API key is detected, the engine gracefully falls back to an internal deterministic parsing mode — the dashboard remains 100% functional without crashing.

### 3. Initialize the Local MSME Database

Generate the 105 synthetic MSME profiles (spanning Healthy NTC Retailers, Distressed NTB Manufacturers, and informal Micro-Enterprises):

```bash
python data/synthetic_generator.py
```

### 4. Launch the Dashboard

```bash
streamlit run app/streamlit_dashboard.py
```

---

## 💡 Operational Test Personas

Use the sidebar selector in the dashboard to toggle between predefined archetypes and observe how the multi-agent engine responds:

- **Healthy NTC Retailer (High UPI, No Bureau History)** — Scores high on the Cash Flow pillar due to elevated UPI volumes and stable GST filings. The system overrides the absence of traditional bureau history to grant an **Approved** status at a prime interest rate.
- **Distressed NTB Manufacturer (High Risk)** — Triggers penalties in the Transaction Maturity and Revenue pillars due to declining MoM sales, contracting headcount, vendor concentration above 65%, and frequent cheque bounces. Flags **Critical Risk** and produces an automated rejection.
- **Micro-Enterprise without EPFO** — Tests robustness against missing data nodes. The pipeline bypasses the empty EPFO channel without exceptions, calculating a micro-capital credit facility from UPI cash-flow signals alone.

---

## ⚙️ Tech Stack

- **Language:** Python
- **LLM Inference:** Groq API (LLaMA 3.3 70B)
- **Frontend:** Streamlit
- **Data Layer:** Synthetic MSME persona generator (JSON/mock ULI-AA payloads)
- **Architecture Pattern:** Multi-agent, deterministic-first with LLM used only for narrative synthesis (not scoring math)

---

## 📌 Notes

- All financial scoring math is deterministic and rule-based; the LLM is used exclusively to generate the human-readable Underwriting Memo, eliminating hallucination risk in the actual credit decision.
- Designed to be demo-ready with zero external dependencies beyond an optional Groq API key.