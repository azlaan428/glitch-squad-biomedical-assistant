# ARIA Project Status

## What Was Built

Multi-agent pipeline in agent/agent.py with 4 stages:
1. Query Architect: generates 5 MeSH-optimised PubMed queries via Groq
2. Literature Scout: fetches all queries sequentially with rate limiting
3. Evidence Synthesiser: structured synthesis with Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications
4. Citation Builder: formatted references with PMID

Additional features:
- SSE streaming: real-time progress bar updates as each stage completes
- Evidence confidence scoring: green/yellow/red badges on each synthesis section
- Abstract viewer: click any citation to expand full abstract inline
- PDF export: download formatted report via ReportLab
- run.sh: clean restart script that kills zombie processes

## Tech Stack
- LLM: Groq LLaMA-3.1-8B-Instant (zero CPU load)
- Agent Framework: LangGraph + LangChain
- Literature Retrieval: BioPython Entrez / PubMed NCBI
- Web Framework: Flask with SSE streaming
- PDF: ReportLab
- Frontend: HTML, CSS, vanilla JS

## Groq API Key
Stored in ~/.bashrc as GROQ_API_KEY environment variable

## What Remains

### High Priority (build next)
1. Selective literature review — checkboxes on citations, user picks papers, generates focused academic literature review from selection
2. Predictive model (constructive) — given retrieved papers, predict where the field is heading
3. Predictive model (destructive) — identify which current assumptions the evidence suggests may be overturned
4. Concept document for lablab.ai submission
5. Demo video (under 3 minutes)
6. LinkedIn post with #AMDDevHackathon
7. Submit on lablab.ai before May 10

### Lower Priority
- Humanizer pass (5th agent stage for flowing prose)
- PICO formatter
- Query history sidebar
- AMD MI300X swap (Mistral 7B) when credits arrive

## GitHub
github.com/azlaan428/glitch-squad-biomedical-assistant

## Deadline
May 10 — lablab.ai submission
