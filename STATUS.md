# ARIA Project Status

## What Was Built

Multi-agent pipeline in agent/agent.py with 4 stages:
1. Query Architect: generates 5 MeSH-optimised PubMed queries via Groq
2. Literature Scout: fetches all queries sequentially with rate limiting
3. Evidence Synthesiser: structured synthesis with Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications
4. Citation Builder: formatted references with PMID

Additional features completed:
- SSE streaming: real-time progress bar updates as each stage completes
- Evidence confidence scoring: green/yellow/red badges on each synthesis section
- Abstract viewer: click any citation to expand full abstract inline
- PDF export: download formatted report via ReportLab
- Selective literature review: checkboxes on citations, user picks papers, generates focused academic paragraph
- Predictive model: constructive and destructive forecasts as a post-synthesis stage
- Session history: queries saved to sessions.json, reloadable from sidebar
- Evidence comparison table: LLM extracts structured data table from synthesis
- Signature: Azlaan Mohammad 2026 in footer
- run.sh: clean restart script

## Tech Stack
- LLM: Groq LLaMA-3.1-8B-Instant
- Agent Framework: LangGraph + LangChain
- Literature Retrieval: BioPython Entrez / PubMed NCBI
- Web Framework: Flask with SSE streaming
- PDF: ReportLab
- Frontend: HTML, CSS, vanilla JS

## API Endpoints
- GET  /           — main UI
- GET  /stream     — SSE pipeline stream
- POST /query      — standard pipeline (fallback)
- POST /score      — confidence scoring
- POST /predict    — predictive model
- POST /selective-review — focused literature review from selected papers
- POST /extract-table    — evidence comparison table
- POST /export-pdf       — PDF report download
- GET  /sessions         — load query history
- POST /sessions/save    — save completed query

## Groq API Key
Stored in ~/.bashrc as GROQ_API_KEY environment variable

## What Remains Before May 10
1. Concept document for lablab.ai submission
2. Demo video (under 3 minutes)
3. LinkedIn post with #AMDDevHackathon
4. Submit on lablab.ai before May 10

## GitHub
github.com/azlaan428/glitch-squad-biomedical-assistant

## Deadline
May 10 - lablab.ai submission
