# Agentic Predictive Maintenance with Multi-Agent RAG 🛠️🤖

An **Agentic Multi-Agent AI System** for industrial predictive maintenance. Three specialized AI agents collaborate to analyze IoT sensor data, retrieve relevant technical documentation via **Advanced RAG**, and generate professional maintenance reports — all orchestrated through a unified pipeline.

---

## 🏗️ System Architecture

```
                          ┌─────────────────────────────┐
                          │      Sensor Data (IoT)       │
                          │  vibration, acoustic, temp,  │
                          │   current, IMF_1, IMF_2...   │
                          └──────────────┬──────────────┘
                                         │
                          ┌──────────────▼──────────────┐
                          │   🔵 Agent 1: SensorAnalyst  │
                          │   (Rule-Based, No LLM)       │
                          │   • Threshold classification  │
                          │   • Failure mode detection    │
                          │   • IMF signal analysis       │
                          └──────────────┬──────────────┘
                                         │ Anomaly Report (dict)
                          ┌──────────────▼──────────────┐
                          │ 🟡 Agent 2: KnowledgeRetriever│
                          │   (Semantic Search, No LLM)   │
                          │   • ChromaDB vector search    │
                          │   • Context-aware query build │
                          │   • Relevant doc retrieval    │
                          └──────────────┬──────────────┘
                                         │ Retrieved Docs (str)
                          ┌──────────────▼──────────────┐
                          │ 🔴 Agent 3: MaintenancePlanner│
                          │   (LLM-Powered via Groq)      │
                          │   • Report synthesis          │
                          │   • Root cause analysis       │
                          │   • Action plan generation    │
                          └──────────────┬──────────────┘
                                         │
                          ┌──────────────▼──────────────┐
                          │  📋 Professional Maintenance  │
                          │        Report Output          │
                          └─────────────────────────────┘
```

---

## 🌟 Key Features

- **Multi-Agent Orchestration**: Three specialized agents with distinct responsibilities, coordinated by a central orchestrator with execution logging and performance tracking.
- **Advanced RAG Architecture**: Technical manuals are chunked and indexed in ChromaDB using semantic embeddings (`all-MiniLM-L6-v2`). Only the most relevant sections are retrieved for each anomaly — not the entire manual.
- **Hybrid Intelligence Design**: Deterministic agents (rule-based threshold checks) handle precision-critical tasks, while LLM is reserved for interpretation and natural language generation — minimizing hallucination risk.
- **Gateway Pattern**: All LLM communication flows through a single gateway function, enabling provider-agnostic design (swap Groq → OpenAI → Gemini with one line change).
- **Automated RCA**: Root Cause Analysis by mapping sensor patterns to specific failure modes (Bearing Failure, Overload, Acoustic Resonance).
- **IMF Signal Analysis**: Advanced monitoring of Intrinsic Mode Functions for early structural crack detection.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **LLM** | Llama 3.3 70B via Groq API (free tier) |
| **Vector Database** | ChromaDB (persistent, local) |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` (Sentence-Transformers) |
| **Data Processing** | Python, Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **UI Framework** | Streamlit (Coming Soon) |

---

## 📊 Methodology

### 1. Exploratory Data Analysis (Notebook 01)
- Statistical profiling of 1,800 IoT sensor readings across 3 machines (M01, M02, M03)
- Correlation analysis revealing vibration (0.78) as the strongest failure predictor
- Class imbalance assessment: 202 failures vs 1,598 normal readings (11.2% failure rate)
- Single-query LLM diagnosis test via Groq API

### 2. RAG Pipeline Setup (Notebook 02)
- Technical manual chunking using `##` header-based splitting (10 semantic chunks)
- Vector embedding and indexing in ChromaDB with persistent storage
- Semantic search validation — confirming correct document retrieval for anomaly queries

### 3. Multi-Agent System (Notebook 03)
- **SensorAnalystAgent**: Rule-based parameter classification (Normal/Elevated/Warning/Critical) and failure mode detection against technical manual thresholds
- **KnowledgeRetrieverAgent**: Dynamic query construction from anomaly reports, semantic search in ChromaDB
- **MaintenancePlannerAgent**: LLM-powered report synthesis combining sensor analysis with retrieved technical documentation
- **MultiAgentOrchestrator**: Sequential pipeline execution with per-step timing and structured logging
- Batch analysis across 5 failure samples with comparative results table

---

## 📁 Project Structure

```
predictive-maintenance-multi-agent/
│
├── data/
│   ├── raw/                        # Raw IoT sensor datasets
│   │   └── predictive_maintenance_dataset.csv
│   └── db/                         # ChromaDB persistent storage
│
├── docs/
│   └── technical_manual.md         # Alpha-V8 Machine Technical Manual
│
├── notebooks/
│   ├── 01_eda_and_data_profiling.ipynb    # EDA & initial LLM diagnosis
│   ├── 02_vector_db_and_rag_setup.ipynb   # ChromaDB & RAG pipeline
│   └── 03_multi_agent_system.ipynb        # Multi-Agent orchestration
│
├── src/                            # Core agent modules (refactored)
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Free Groq API key ([console.groq.com](https://console.groq.com))

### Installation

```bash
git clone https://github.com/fhattat/Agentic-Predictive-Maintenance.git
cd Agentic-Predictive-Maintenance
pip install -r requirements.txt
```

### Configuration
Create a `.env` file or directly set your API key in the notebooks:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Run
Execute notebooks in order:
```
01_eda_and_data_profiling.ipynb  →  02_vector_db_and_rag_setup.ipynb  →  03_multi_agent_system.ipynb
```

---

## 📈 Results

### Pipeline Performance (Sample)
| Agent | Duration | Output |
| :--- | :--- | :--- |
| SensorAnalyst | ~0.001s | Risk level + parameter status + failure modes |
| KnowledgeRetriever | ~0.05s | Top 3 relevant manual sections |
| MaintenancePlanner | ~3-5s | Professional maintenance report |

### Detected Failure Modes
The system correctly identifies three failure types defined in the technical manual:
- **Tip A**: Mechanical Fatigue & Bearing Failure (Vibration > 1.25 AND Acoustic > 0.90)
- **Tip B**: Electrical Overload & Overheating (Current > 15.0A AND Temperature > 80°C)
- **Tip C**: Acoustic Resonance / Loose Component (Acoustic spike > 1.10, others normal)

---

## 🎯 AI Engineering Design Decisions

| Decision | Rationale |
| :--- | :--- |
| No LLM in SensorAnalyst | Threshold checks are deterministic — LLM hallucination risk is unnecessary |
| Semantic search in KnowledgeRetriever | Sending the entire manual wastes tokens and dilutes relevance |
| LLM only in MaintenancePlanner | LLM excels at interpretation and synthesis — we use it where it adds the most value |
| Gateway Pattern for LLM calls | Provider change (Groq → OpenAI → Gemini) requires only one line change |
| Structured inter-agent communication | Dict-based data flow enables debugging, logging, and future agent additions |

---

## 🗺️ Roadmap

- [x] Exploratory Data Analysis & initial diagnosis
- [x] RAG pipeline with ChromaDB
- [x] Multi-Agent system with 3 specialized agents
- [ ] Streamlit interactive dashboard
- [ ] Agent memory & conversation history
- [ ] Docker containerization
- [ ] Deployment on Hugging Face Spaces

---

## 👤 Author

**Dr. Fatih Hattatoglu**
- LinkedIn: [fatih-hattatoglu-phd](https://tr.linkedin.com/in/fatih-hattatoglu-phd)
- GitHub: [fhattat](https://github.com/fhattat)
- Medium: [fhattat.medium.com](https://fhattat.medium.com)
- Portfolio: [drfatih.netlify.app](https://drfatih.netlify.app)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
