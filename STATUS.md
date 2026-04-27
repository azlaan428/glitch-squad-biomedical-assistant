# ARIA Project Status

## What Was Built
- Multi-agent pipeline (agent/agent.py) with 4 stages:
  1. Query Architect: generates 5 MeSH-optimised PubMed queries via Groq
  2. Literature Scout: sequential PubMed fetch with 0.4s delay (429 fix)
  3. Evidence Synthesiser: structured synthesis (Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications)
  4. Citation Builder: formatted references with real title/authors/journal/year parsed from raw PubMed text
- Groq API (llama-3.1-8b-instant) - zero CPU load
- Flask backend with /query (POST) and /stream (SSE GET) and /export-pdf (POST) endpoints
- SSE streaming: progress bar animates through real pipeline stages in real time
- PDF export via reportlab
- Dark theme UI with collapsible synthesis sections, progress bar with percentage
- run.sh for clean server restart

## Groq API Key
Stored in ~/.bashrc as GROQ_API_KEY

## What Remains
1. Paper selection feature: checkboxes on citations, generate targeted literature review from selected papers
2. Predictive model as Agent 5: constructive/destructive research trajectory prediction
3. Evidence confidence scoring (green/yellow/red per section)
4. Abstract viewer (click citation to expand inline)
5. Concept document for lablab.ai
6. Demo video (under 3 min)
7. LinkedIn post with #AMDDevHackathon
8. Submit on lablab.ai before May 10
9. AMD MI300X swap (Mistral 7B) when credits arrive

## GitHub
github.com/azlaan428/glitch-squad-biomedical-assistant
