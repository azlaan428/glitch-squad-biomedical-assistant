# ARIA Project Status
_Last updated: May 3, 2026_

## What Was Built

Multi-agent pipeline in agent/agent.py with 5 stages:

1. Query Architect: generates 5 MeSH-optimised PubMed queries via Groq
2. Literature Scout: fetches all queries sequentially with rate limiting
3. PRISMA Filter: automatic inclusion/exclusion screening with one-line reasons, user can override any decision
4. Evidence Synthesiser: structured synthesis with Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications
5. Citation Builder: formatted references with PMID, synthesis runs on PRISMA-included papers only

Additional features completed:

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
* Rate limit retry logic: automatic backoff on Groq 429 errors
* SSL patch for PubMed Entrez on corporate/university networks
* Signature: Azlaan Mohammad 2026 in footer

## UI Updates (May 3 2026)

* PRISMA screening panel with cyan/red inclusion dots and override buttons
* Follow-up Q&A input block appears after synthesis
* Suggested follow-up queries panel with clickable buttons
* Evidence table with real author surnames replacing placeholder text

## UI Updates (Apr 29 2026)

* Rebranded color scheme: ARIA Cyan (#00f5ff) replacing teal accent
* New fonts: Inter (sans) + JetBrains Mono replacing IBM Plex
* Animated hexagonal SVG logo with "A" monogram in header
* Animated gradient mesh background replacing flat grid

## Tech Stack

* LLM: Groq LLaMA-3.1-8B-Instant (migration to Llama 3.3 70B on AMD MI300X planned)
* Agent Framework: LangGraph + LangChain
* Literature Retrieval: BioPython Entrez / PubMed NCBI
* Web Framework: Flask with SSE streaming
* PDF: ReportLab
* Frontend: HTML, CSS, vanilla JS
* Runtime: Windows 11, Python 3.11, RTX 3060 12GB

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

* GROQ_API_KEY set via $env:GROQ_API_KEY in PowerShell
* Python venv at ./venv
* Start server: venv\Scripts\activate && python app.py
* AMD MI300X credits available on lablab.ai (instance not yet spun up)

## What Remains Before May 11

1. Spin up AMD MI300X instance and migrate inference to vLLM + Llama 3.3 70B
2. Concept document for lablab.ai submission (window opens May 11)
3. Demo video (under 3 minutes)
4. LinkedIn post with #AMDDevHackathon
5. Submit on lablab.ai

## GitHub

github.com/azlaan428/glitch-squad-biomedical-assistant

## Deadline

May 11 — lablab.ai submission window opens
