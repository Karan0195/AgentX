# AgentX: Autonomous Multi-Agent Data Intelligence & Multimodal Analytics Platform

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.1-orange.svg)](https://flask.palletsprojects.com/)
[![Query Engine](https://img.shields.io/badge/Query%20Engine-DuckDB-yellow.svg)](https://duckdb.org/)
[![LLM](https://img.shields.io/badge/LLM-Groq%20%2F%20LLaMA%203-red.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

AgentX is an autonomous, multi-agent AI data science and business intelligence copilot. It allows technical analysts and business leaders alike to upload multi-format structured datasets (CSV, TSV, Excel, Parquet, JSON) and unstructured documents (PDFs, scanned mark sheets, voter lists), ask questions in natural human language (English, Hindi, Hinglish, Marathi), and receive grounded, mathematically verified calculations, interactive data tables, publication-grade Matplotlib charts, and executive intelligence reports.

---

## Key Features

- **Multi-Agent Collaborative Architecture:** Powered by a network of specialized agents (`Orchestrator`, `QueryUnderstandingAgent`, `CodeExecutionEngine`, `CriticAgent`, `AnalystAgent`, `VisualizationAgent`, `ReportAgent`).
- **Autonomous Self-Healing Code Execution:** Dynamically writes Python/Pandas code in a secure sandbox. If runtime syntax or indexing errors occur, the engine captures tracebacks and self-corrects up to 3 times automatically.
- **Critic Agent (Zero-Hallucination Guarantee):** Validates column choices, checks numerical boundaries, ensures percentage constraints (0-100%), and assigns confidence scores before presenting results.
- **Multimodal Document Engine:** Reads multi-page PDFs and scanned images via embedded RapidOCR and PyMuPDF, with phonetic Devanagari transliteration for regional language rosters.
- **Universal Ingestion:** Auto-detects delimiters (comma, tab, semicolon, pipe) and character encodings (`charset-normalizer`) across multi-sheet workbooks.
- **Modern Glassmorphism UI:** Features interactive dataset staging (`Ready to Upload` -> `Upload Now`), one-click dataset unloading (`Remove Dataset`), real-time bottom telemetry cards, and downloadable HTML reports.

---

## Multi-Agent Architecture

```text
                                 [ User Query ]
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │    Orchestrator     │
                            └──────────┬──────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        [ Tabular Pipeline ]                    [ Document Pipeline ]
                │                                         │
    ┌───────────┴───────────┐                 ┌───────────┴───────────┐
    │ QueryUnderstanding    │                 │   DocumentEngine      │
    │ (Typo/Hinglish/Syn)   │                 │ (PyMuPDF / RapidOCR)  │
    └───────────┬───────────┘                 └───────────┬───────────┘
                ▼                                         ▼
    ┌───────────────────────┐                 ┌───────────────────────┐
    │  CodeExecutionEngine  │                 │       LLMAgent        │
    │  (Self-Healing Loop)  │                 │    (Grounded QA)      │
    └───────────┬───────────┘                 └───────────┬───────────┘
                ▼                                         │
    ┌───────────────────────┐                             │
    │  VisualizationAgent   │                             │
    │  (Matplotlib Charts)  │                             │
    └───────────┬───────────┘                             │
                │                                         │
                └──────────────────┬──────────────────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │     CriticAgent     │
                        │ (Verification & QA) │
                        └──────────┬──────────┘
                                   │
                                   ▼
                       [ Verified Chat Answer ]
```

---

## Project Structure

```text
AgentX/
├── agents/
│   ├── analyst_agent.py          # Data profiling, EDA, and statistical metrics
│   ├── code_execution_engine.py  # Sandboxed Python execution & self-healing loop
│   ├── critic_agent.py           # Verification guardian and boundary auditor
│   ├── data_agent.py             # Schema inspection and DuckDB interface
│   ├── llm_agent.py              # Groq LLaMA 3 client wrapper
│   ├── orchestrator.py           # Central multi-agent coordinator
│   ├── query_understanding.py    # Typo correction, Hinglish, & synonym matcher
│   ├── report_agent.py           # Executive HTML report generator
│   └── visualization_agent.py    # Dynamic Matplotlib chart generator
├── data/
│   ├── agentx.db                 # SQLite relational database (auth, history, records)
│   └── students_dataset.csv      # Sample verification dataset
├── templates/
│   ├── index.html                # Main interactive analytics dashboard
│   └── login.html                # Authentication portal (login, signup, reset)
├── utils/
│   ├── auth_db.py                # Database connection, schemas, and password hashing
│   ├── data_engine.py            # Universal tabular loader (CSV, Excel, Parquet, JSON)
│   └── document_engine.py        # PDF extraction, OCR fallback, Indic transliteration
├── app.py                        # Flask server, API endpoints, and bootstrap loader
├── config.py                     # Configuration settings and environment loader
├── requirements.txt              # Production dependencies
├── .env.example                  # Environment configuration template
└── README.md                     # Documentation
```

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/AgentX.git
cd AgentX
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
PROJECT_NAME=AgentX
GROQ_API_KEY=your_groq_api_key_here
```
*(Get a free API key at [console.groq.com](https://console.groq.com/keys))*

### 5. Launch the Application
```bash
python app.py
```
Open your browser to `http://127.0.0.1:5000`.

---

## Running Automated Tests
```bash
pytest tests/
```

---

## License
Distributed under the MIT License. See `LICENSE` for more information.

