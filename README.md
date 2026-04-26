# Glitch Squad Biomedical Assistant

A biomedical AI research assistant that retrieves live literature from PubMed and synthesises responses using a LangGraph ReAct agent powered by Llama 3.2.

Built for the AMD Developer Hackathon 2026.

---

## What It Does

You type a biomedical research question. The agent autonomously searches PubMed for relevant abstracts, reasons over the retrieved literature, and returns a synthesised answer with PMID citations.

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Llama 3.2 via Ollama (local) / Mistral 7B on AMD MI300X (cloud) |
| Agent Framework | LangGraph prebuilt ReAct agent |
| Literature Retrieval | BioPython Entrez / NCBIPubMed API |
| Web Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Runtime | Python 3.12, WSL2 Ubuntu 24.04 |

---

## How To Run Locally

### Prerequisites
- Python 3.12
- Ollama installed
- llama3.2 model pulled: `ollama pull llama3.2`

### Setup

    git clone https://github.com/azlaan428/glitch-squad-biomedical-assistant.git
    cd glitch-squad-biomedical-assistant
    python3 -m venv _venv
    source venv/bin/activate
    pip install -r requirements.txt

### Run

    ollama serve &
    python app.py

Open your browser at http://localhost:5000

---

## Team

**Glitch Squad** -- Ziauddin University, Karachi, Pakistan
