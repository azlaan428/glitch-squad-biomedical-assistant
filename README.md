---
title: ARIA - Research Synthesis & Integrity Auditor
emoji: 🧬
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# ARIA — Autonomous Research Intelligence Agent

> Multi-agent research synthesis and integrity auditing · originally built for the AMD Developer Hackathon 2026
> **Team Glitch Squad** — Ziauddin University, Karachi, Pakistan

---

## What It Does

ARIA is a multi-agent pipeline that takes a research question, retrieves literature, synthesises it into a structured report, and then — on demand — runs a second layer of agents that audit that synthesis for citation accuracy, methodological consistency, and reproducibility.

The pipeline and audit logic are domain-agnostic. The current live demo is wired to **biomedical literature via PubMed and Europe PMC**, but nothing about the architecture is biomedical-specific — swapping the retrieval source and prompts would repoint it at any other literature corpus.

## Pipeline (5 stages)

```
Query Architect → Literature Scout → PRISMA Filter → Evidence Synthesiser → Citation Builder
```

1. **Query Architect** — generates up to 5 MeSH-optimised search queries from your research question
2. **Literature Scout** — fetches each query against PubMed (Entrez, up to 5 results) and Europe PMC (up to 3 results), deduplicating by PMID
3. **PRISMA Filter** — screens every retrieved paper as included/excluded against the question, with a one-line reason for each exclusion
4. **Evidence Synthesiser** — builds a structured 6-section synthesis (Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications) with inline PMID citations, using only PRISMA-included papers
5. **Citation Builder** — formats a numbered reference list (authors, journal, year, PMID)

## Integrity Audit (5 agents)

Run on demand after synthesis via the "Run Integrity Audit" button. Results are grouped into **Internal Consistency** and **External Validity**, same as the UI:

**Internal Consistency**
- **Methodology Drift Tracker** — checks whether a paper's stated methodology actually matches its own reported results
- **Confidence Calibration Check** — checks whether the language strength of a synthesis claim matches the actual strength of the evidence behind it

**External Validity**
- **Citation Ghost Detector** — checks every PMID-cited claim in the synthesis against the source abstract it cites
- **Cross-Paper Contradiction Finder** — compares findings across pairs of retrieved papers for agreement or contradiction
- **Reproducibility Score** — scores each paper 0–100 on whether it reports sample size, statistical methods, data/code/materials availability, and inclusion/exclusion criteria

## UI

A sticky, collapsible side-panel with six tabs: **Main**, **Integrity Audit**, **PRISMA**, **References**, **Comparison**, **Follow-up**.

## Other features

- Real-time SSE streaming — progress bar updates as each pipeline stage completes
- Evidence confidence scoring — green/yellow/red badges on each synthesis section, from a second LLM pass
- Abstract viewer — click any citation to expand the full abstract inline
- Evidence comparison table — LLM-extracted structured table of studies/methods/outcomes
- Selective literature review — check specific citations and generate a focused academic paragraph from just those papers
- Predictive forecasting — constructive and destructive forecasts derived from the synthesised evidence
- Follow-up Q&A — ask follow-up questions answered from the already-fetched papers, no re-fetching
- Query refinement suggestions — 3 AI-generated follow-up research questions based on synthesis gaps
- Session history — queries saved to `sessions.json`, reloadable from the sidebar
- **PDF export** — synthesis, evidence comparison table, PRISMA exclusions (with reasons), and the full Integrity Audit, all in one report. Tables and audit cards are page-break-safe: reportlab only starts a new page when a table/card wouldn't fit on the current one, never splitting a row or card across the boundary.

## Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | **Groq — `llama-3.1-8b-instant` (active)**. The pipeline previously ran on Qwen2.5-72B-Instruct via vLLM on a rented AMD MI300X during the hackathon, then was reverted to Groq for reliability. That code path no longer exists in the tree — swapping back means rewriting `get_llm()` in `agent/agent.py` (it's a ~5 line change, see git history at `7dd2c52`/`f81857a`) and standing up an inference endpoint again. |
| Agent Framework | LangGraph + LangChain |
| Literature Retrieval | BioPython Entrez (PubMed) + Europe PMC REST API |
| Web Framework | Flask, SSE streaming |
| PDF Generation | ReportLab |
| Frontend | HTML, CSS, vanilla JS |
| Deployment | Docker container on Hugging Face Spaces |

## Setup

```bash
git clone https://github.com/azlaan428/glitch-squad-biomedical-assistant.git
cd glitch-squad-biomedical-assistant
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set your Groq API key (required — the app raises an error at request time if it's missing):

```bash
export GROQ_API_KEY=your_key_here      # Windows PowerShell: $env:GROQ_API_KEY = "your_key_here"
```

## Run

```bash
python app.py
```

Open http://localhost:7860 (default port, overridable via the `PORT` env var — this is what the Dockerfile also sets for Hugging Face Spaces).

> Groq's free tier rate-limits fairly aggressively. Every LLM call in the pipeline retries with backoff on a 429, but a query against a large paper set can still take a couple of minutes if it has to back off repeatedly.

## Live Demo

https://huggingface.co/spaces/azlaan428/glitch-squad-biomedical-assistant

## Disclaimer

AI-generated synthesis — always verify against primary sources before clinical or other high-stakes use.
