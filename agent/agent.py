import sys, os, re
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from retrieval.pubmed import fetch_pubmed


def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=os.environ.get("GROQ_API_KEY")
    )


@tool
def PubMedSearch(query: str) -> str:
    """Searches PubMed for biomedical literature abstracts."""
    results = fetch_pubmed(query, max_results=5)
    if not results:
        return "No abstracts found for this query."
    out = []
    for r in results:
        out.append("[PMID " + r["pmid"] + "]\n" + r["abstract"])
    return "\n\n".join(out)


def run_query_architect(user_question):
    llm = get_llm()
    prompt = (
        "You are a biomedical librarian expert in PubMed search strategy.\n"
        "Given this clinical question, generate exactly 5 distinct PubMed search queries using "
        "MeSH terminology and clinical keywords to maximise literature coverage.\n"
        "Return ONLY a numbered list 1-5, one query per line, no explanations.\n\n"
        "Question: " + user_question
    )
    response = llm.invoke(prompt)
    raw_lines = response.content.strip().split("\n")
    queries = []
    for line in raw_lines:
        clean = re.sub(r"^[\d]+[\.)\s]+", "", line.strip())
        if clean:
            queries.append(clean)
    return queries[:5]


def run_literature_scout(queries):
    all_papers = {}
    def fetch_one(q):
        return fetch_pubmed(q, max_results=5)
    import time
    for q in queries:
        time.sleep(0.4)
        for r in fetch_one(q):
            if r["pmid"] not in all_papers:
                all_papers[r["pmid"]] = r
    return all_papers


def run_evidence_synthesiser(user_question, papers):
    llm = get_llm()
    parts = []
    for pmid, p in list(papers.items())[:6]:
        title = p.get("title", "N/A")
        abstract = p["abstract"]
        parts.append("[PMID " + pmid + "]\nTitle: " + title + "\n" + abstract)
    corpus = "\n\n".join(parts)
    prompt = (
        "You are a senior biomedical researcher writing a structured evidence synthesis.\n"
        "Answer the clinical question using ONLY this structure:\n\n"
        "## Background\n"
        "Brief context (2-3 sentences).\n\n"
        "## Key Findings\n"
        "Most important findings with PMID citations inline.\n\n"
        "## Level of Evidence\n"
        "Rate: Strong / Moderate / Preliminary. Justify briefly.\n\n"
        "## Conflicting Evidence\n"
        "Any contradictions across studies.\n\n"
        "## Research Gaps\n"
        "What the literature does not answer.\n\n"
        "## Clinical Implications\n"
        "What this means for practice or future research.\n\n"
        "Clinical Question: " + user_question + "\n\n"
        "Retrieved Literature:\n" + corpus + "\n\n"
        "Be precise and cite PMIDs throughout."
    )
    response = llm.invoke(prompt)
    return response.content


def run_citation_builder(papers):
    result_lines = []
    for i, (pmid, p) in enumerate(papers.items(), 1):
        title = p.get("title", "Title unavailable")
        authors = p.get("authors", "Authors unavailable")
        journal = p.get("journal", "Journal unavailable")
        year = p.get("year", "n.d.")
        result_lines.append(
            str(i) + ". " + authors + " (" + year + "). " + title + ". " + journal + ". PMID: " + pmid
        )
    return "\n".join(result_lines)



def run_confidence_scorer(synthesis):
    llm = get_llm()
    prompt = (
        "You are a critical appraiser of biomedical evidence.\n"
        "Given this synthesis, score each section for evidence quality.\n"
        "Return ONLY valid JSON, no markdown, no explanation:\n"
        "{\n"
        '  "Background": {"score": 8, "rationale": "one sentence"},\n'
        '  "Key Findings": {"score": 7, "rationale": "one sentence"},\n'
        '  "Level of Evidence": {"score": 6, "rationale": "one sentence"},\n'
        '  "Conflicting Evidence": {"score": 5, "rationale": "one sentence"},\n'
        '  "Research Gaps": {"score": 7, "rationale": "one sentence"},\n'
        '  "Clinical Implications": {"score": 6, "rationale": "one sentence"}\n'
        "}\n\n"
        "Scores: 8-10 = strong evidence, 5-7 = moderate, 1-4 = weak/preliminary.\n\n"
        "Synthesis:\n" + synthesis
    )
    response = llm.invoke(prompt)
    import json
    text = response.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def run_pipeline(user_question):
    print("[1/4] Query Architect: generating search queries...")
    queries = run_query_architect(user_question)
    print("      Generated " + str(len(queries)) + " queries")
    print("[2/4] Literature Scout: fetching PubMed in parallel...")
    papers = run_literature_scout(queries)
    print("      Retrieved " + str(len(papers)) + " unique papers")
    print("[3/4] Evidence Synthesiser: building structured synthesis...")
    synthesis = run_evidence_synthesiser(user_question, papers)
    print("[4/4] Citation Builder: formatting references...")
    citations = run_citation_builder(papers)
    return {
        "question": user_question,
        "queries": queries,
        "paper_count": len(papers),
        "synthesis": synthesis,
        "citations": citations,
        "papers": papers
    }


def build_agent():
    llm = get_llm()
    return create_react_agent(llm, [PubMedSearch])


if __name__ == "__main__":
    question = "What are the most effective ML methods for epilepsy seizure detection from EEG signals?"
    result = run_pipeline(question)
    print("\n=== SYNTHESIS ===")
    print(result["synthesis"])
    print("\n=== REFERENCES ===")
    print(result["citations"])
