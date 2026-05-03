# \# ARIA Project Status

# \_Last updated: May 3, 2026\_

# 

# \## What Was Built

# 

# Multi-agent pipeline in `agent/agent.py` with 5 stages:

# 

# 1\. \*\*Query Architect\*\* — generates 5 MeSH-optimised PubMed queries via Groq

# 2\. \*\*Literature Scout\*\* — fetches all queries sequentially with rate limiting

# 3\. \*\*PRISMA Filter\*\* — automatic inclusion/exclusion screening with one-line reasons, user can override any decision

# 4\. \*\*Evidence Synthesiser\*\* — structured synthesis: Background, Key Findings, Level of Evidence, Conflicting Evidence, Research Gaps, Clinical Implications

# 5\. \*\*Citation Builder\*\* — formatted references with PMID, synthesis runs on PRISMA-included papers only

# 

# \### Features Completed

# 

# \- SSE streaming: real-time 5-stage progress bar with percentage

# \- PRISMA-style paper screening: automated include/exclude with rationale, user override buttons

# \- Evidence confidence scoring: green/yellow/red badges on each synthesis section with hover tooltips

# \- Abstract viewer: click any citation to expand full abstract inline

# \- PDF export: formatted ReportLab report download

# \- Selective literature review: checkboxes on citations, generates focused academic paragraph from selected papers

# \- Predictive model: constructive and destructive forecasts as a post-synthesis stage

# \- Evidence comparison table: LLM extracts structured data table from synthesis, with real author names and no duplicate rows

# \- Follow-up Q\&A: ask follow-up questions after synthesis, answered using already-fetched papers

# \- Query refinement suggestions: 3 AI-generated follow-up research questions based on synthesis gaps

# \- Session history: queries saved to sessions.json, reloadable from sidebar

# \- Rate limit retry logic: automatic backoff on Groq 429 errors

# \- SSL patch for PubMed Entrez on corporate/university networks

# \- Signature: Azlaan Mohammad 2026 in footer

# 

# \### UI

# 

# \- ARIA Cyan (#00f5ff) color scheme

# \- Inter (sans) + JetBrains Mono fonts

# \- Animated hexagonal SVG logo with "A" monogram

# \- Grid mesh background

# \- Fixed history sidebar panel

# 

# \## Tech Stack

# 

# \- \*\*LLM\*\*: Groq LLaMA-3.1-8B-Instant (migration to Llama 3.3 70B on AMD MI300X planned)

# \- \*\*Agent Framework\*\*: LangGraph + LangChain

# \- \*\*Literature Retrieval\*\*: BioPython Entrez / PubMed NCBI

# \- \*\*Web Framework\*\*: Flask with SSE streaming

# \- \*\*PDF\*\*: ReportLab

# \- \*\*Frontend\*\*: HTML, CSS, vanilla JS

# \- \*\*Runtime\*\*: Windows 11, Python 3.11, RTX 3060 12GB

# 

# \## API Endpoints

# 

# | Method | Route | Description |

# |--------|-------|-------------|

# | GET | `/` | Main UI |

# | GET | `/stream` | SSE pipeline stream |

# | POST | `/query` | Standard pipeline (fallback) |

# | POST | `/score` | Confidence scoring |

# | POST | `/predict` | Predictive model |

# | POST | `/selective-review` | Focused literature review from selected papers |

# | POST | `/extract-table` | Evidence comparison table |

# | POST | `/export-pdf` | PDF report download |

# | POST | `/followup` | Follow-up question against existing synthesis |

# | POST | `/suggest-queries` | 3 AI-generated follow-up research questions |

# | GET | `/sessions` | Load query history |

# | POST | `/sessions/save` | Save completed query |

# 

# \## Environment

# 

# \- `GROQ\_API\_KEY` set via `$env:GROQ\_API\_KEY` in PowerShell session

# \- Python venv at `./venv`

# \- Start server: `venv\\Scripts\\activate \&\& python app.py`

# \- AMD MI300X credits available on lablab.ai (instance not yet spun up)

# 

# \## What Remains Before May 11

# 

# 1\. Spin up AMD MI300X instance and migrate inference to vLLM + Llama 3.3 70B

# 2\. Concept document for lablab.ai submission (window opens May 11)

# 3\. Demo video (under 3 minutes)

# 4\. LinkedIn post with #AMDDevHackathon

# 5\. Submit on lablab.ai

# 

# \## GitHub

# 

# https://github.com/azlaan428/glitch-squad-biomedical-assistant

# 

# \## Deadline

# 

# May 11 — lablab.ai submission window opens

