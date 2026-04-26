# ARIA Project Status

## What Was Built
- Multi-agent pipeline in agent/agent.py with 4 stages:
  1. Query Architect: generates 5 MeSH-optimised PubMed queries via Groq
  2. Literature Scout: fetches all queries in parallel (ThreadPoolExecutor)
  3. Evidence Synthesiser: structured synthesis with Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications
  4. Citation Builder: formatted references with PMID
- Groq API replacing Ollama (llama-3.1-8b-instant) - zero CPU load
- Flask backend (app.py) with /query endpoint
- HTML/CSS/JS frontend with dark theme

## Groq API Key
Stored in ~/.bashrc as GROQ_API_KEY environment variable

## What Remains
1. Update app.py to call run_pipeline() instead of build_agent()
2. Update frontend to display structured synthesis sections properly
3. PDF export (reportlab library)
4. New dashboard UI
5. AMD MI300X swap (Mistral 7B) when credits arrive
6. Concept document
7. Demo video
8. LinkedIn post with #AMDDevHackathon
9. Submit on lablab.ai before May 10

## Next Session Starting Point
Run: cd ~/glitch-squad-biomedical-assistant && source venv/bin/activate
Then tell Claude: "Continue ARIA hackathon project, read STATUS.md"

## GitHub
github.com/azlaan428/glitch-squad-biomedical-assistant
