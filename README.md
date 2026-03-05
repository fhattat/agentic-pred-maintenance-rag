# Agentic Predictive Maintenance with Advanced RAG 🛠️🤖

This project features an **Agentic AI System** designed for industrial predictive maintenance. It combines IoT sensor data analysis with an **Advanced RAG (Retrieval-Augmented Generation)** pipeline to diagnose machine failures and provide actionable maintenance recommendations based on technical manuals.



## 🌟 Key Features
- **Advanced RAG Architecture:** Technical manuals are indexed in **ChromaDB** using semantic embeddings. The system retrieves only the most relevant technical sections for each specific sensor anomaly.
- **Agentic Reasoning:** Powered by **Google Gemini**, the system acts as an "AI Maintenance Engineer," cross-referencing real-time numerical data with retrieved technical documentation.
- **Multimodal Potential:** Built to handle diverse sensor inputs including vibration, acoustics, temperature, and electrical current.
- **Automated RCA:** Performs Root Cause Analysis (RCA) by mapping sensor patterns to specific failure modes (e.g., Bearing Failure, Overload).

## 🛠️ Tech Stack
- **LLM:** Google Gemini 2.0 Flash / 1.5 Pro
- **Vector Database:** ChromaDB
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Sentence-Transformers)
- **Data Orchestration:** Python, Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **UI Framework:** Streamlit (Coming Soon)

## 📊 Methodology
1. **Data Ingestion:** Processing high-frequency IoT sensor data from industrial machinery.
2. **Vectorization:** Chunking and embedding the "Technical Maintenance Manual" into a high-dimensional vector space.
3. **Retrieval:** When an anomaly is detected (e.g., `label=1`), the system queries ChromaDB for relevant safety thresholds and repair procedures.
4. **Agentic Diagnosis:** The LLM receives the sensor "context" + the "retrieved manual parts" to generate a professional maintenance report.



## 📁 Project Structure
- `data/`: Contains raw IoT datasets and the persistent ChromaDB local instance.
- `docs/`: Technical manuals and documentation in Markdown format.
- `notebooks/`: 
    - `01_eda_and_profiling.ipynb`: Exploratory Data Analysis & failure correlation.
    - `02_rag_setup_and_indexing.ipynb`: Vector DB configuration and semantic search testing.
- `src/`: Core logic for the Agentic workflow.

## 🚀 How to Run
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
