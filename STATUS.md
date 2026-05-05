# ARIA Project Status
_Last updated: May 5, 2026_

## What Was Built

Multi-agent pipeline in agent/agent.py with 5 stages:

1. Query Architect: generates 5 MeSH-optimised PubMed queries via Qwen2.5-72B on AMD MI300X
2. Literature Scout: fetches from PubMed and Europe PMC in parallel, deduplicates by PMID
3. PRISMA Filter: automatic inclusion/exclusion screening with one-line reasons, user can override any decision
4. Evidence Synthesiser: structured synthesis with Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications
5. Citation Builder: formatted references with PMID, synthesis runs on PRISMA-included papers only

## Additional Features

* SSE streaming: real-time 5-stage progress bar with percentage
* PRISMA-style paper screening: automated include/exclude with rationale, user override buttons
* Evidence confidence scoring: green/yellow/red badges on each synthesis section with hover tooltips
* Abstract viewer: click any citation to expand full abstract inline
* PDF export: download formatted report via ReportLab
* Selective literature review: checkboxes on citations, user picks papers, generates focused academic paragraph
* Predictive model: constructive and destructive forecasts as a post-synthesis stage
* Evidence comparison table: LLM extracts structured data table with real author names, no duplicates
* Follow-up Q&A: ask follow-up questions after synthesis, answered using already-fetched papers
* Query refinement suggestions: 3 AI-generated follow-up research questions based on synthesis gaps
* Session history: queries saved to sessions.json, reloadable from sidebar
* Rate limit retry logic: automatic backoff on API errors
* SSL patch for PubMed and Europe PMC Entrez on corporate/university networks

## Tech Stack

* LLM: Qwen2.5-72B-Instruct on AMD MI300X via vLLM 0.17.1
* Agent Framework: LangGraph + LangChain
* Literature Retrieval: BioPython Entrez / PubMed NCBI + Europe PMC
* Web Framework: Flask with SSE streaming
* PDF: ReportLab
* Frontend: HTML, CSS, vanilla JS
* Runtime: Windows 11, Python 3.11, RTX 3060 12GB (local) + AMD MI300X 192GB (inference)

## API Endpoints

* GET  /                 — main UI
* GET  /stream           — SSE pipeline stream
* POST /query            — standard pipeline (fallback)
* POST /score            — confidence scoring
* POST /predict          — predictive model
* POST /selective-review — focused literature review from selected papers
* POST /extract-table    — evidence comparison table
* POST /export-pdf       — PDF report download
* POST /followup         — follow-up question against existing synthesis
* POST /suggest-queries  — 3 AI-generated follow-up research questions
* GET  /sessions         — load query history
* POST /sessions/save    — save completed query

## Environment

* VLLM_BASE_URL: set via HF Space environment variable
* VLLM_API_KEY: EMPTY
* Python venv at ./venv
* Start server: venv\Scripts\activate && python app.py
* AMD MI300X: DigitalOcean droplet, 192GB VRAM

## Deployment

* HF Space: https://huggingface.co/spaces/lablab-ai-amd-developer-hackathon/glitch-squad-biomedical-assistant
* GitHub: https://github.com/azlaan428/glitch-squad-biomedical-assistant

## What Remains

1. Demo video (under 5 minutes)
2. Final lablab.ai submission
