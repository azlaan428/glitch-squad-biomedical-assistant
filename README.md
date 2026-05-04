---
title: ARIA - AMD Biomedical Research Intelligence Assistant
emoji: 🧬
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

... your existing README content below ...

# ARIA — Autonomous Research Intelligence Agent

> Multi-agent biomedical literature synthesis · AMD Developer Hackathon 2026
> **Team Glitch Squad** — Ziauddin University, Karachi, Pakistan

---

## What It Does

You type a clinical research question. ARIA runs a 4-stage multi-agent pipeline that searches PubMed, synthesises evidence, scores confidence, and returns a structured report — all in under 60 seconds.

## Pipeline

```
Query Architect  →  Literature Scout  →  Evidence Synthesiser  →  Citation Builder
(Groq LLaMA-3.1)    (PubMed Entrez)      (Groq LLaMA-3.1)        (structured refs)
```

1. **Query Architect** — generates 5 MeSH-optimised PubMed queries from your clinical question
2. **Literature Scout** — fetches and deduplicates papers across all queries in parallel
3. **Evidence Synthesiser** — builds a structured 6-section synthesis with inline PMID citations
4. **Citation Builder** — formats references with authors, journal, year, and PMID

## Features

- Real-time SSE streaming — progress bar updates as each stage completes
- Structured synthesis — Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications
- Evidence confidence scoring — green/yellow/red badges rated by a second LLM pass
- Abstract viewer — click any citation to expand the full abstract inline
- PDF export — download a formatted report with synthesis and references

## Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq LLaMA-3.1-8B-Instant |
| Agent Framework | LangGraph + LangChain |
| Literature Retrieval | BioPython Entrez / PubMed NCBI |
| Web Framework | Flask with SSE streaming |
| PDF Generation | ReportLab |
| Frontend | HTML, CSS, JavaScript |
| Runtime | Python 3.12, WSL2 Ubuntu 24.04 |
| Roadmap | AMD MI300X + Mistral 7B |

## Setup

```bash
git clone https://github.com/azlaan428/glitch-squad-biomedical-assistant.git
cd glitch-squad-biomedical-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
```

## Run

```bash
./run.sh
```

Open **http://localhost:5000**

## Disclaimer

AI-generated synthesis — always verify against primary sources before clinical use.