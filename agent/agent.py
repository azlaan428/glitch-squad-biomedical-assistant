import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from retrieval.pubmed import fetch_pubmed


def pubmed_tool_fn(query: str) -> str:
    results = fetch_pubmed(query, max_results=5)
    if not results:
        return "No abstracts found for this query."
    return "\n\n".join([f"[PMID {r['pmid']}]\n{r['abstract']}" for r in results])

pubmed_tool = Tool(
    name="PubMedSearch",
    func=pubmed_tool_fn,
    description=(
        "Searches PubMed for biomedical literature. "
        "Input should be a clinical or scientific query string. "
        "Returns abstracts relevant to the query."
    )
)

if __name__ == "__main__":
    print("Connecting to Ollama...")
    llm = ChatOllama(model="llama3.2", temperature=0)
    agent = create_react_agent(llm, [pubmed_tool])
    query = "What ML methods are used for epilepsy seizure detection?"
    print(f"\nQuery: {query}\n")
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("\n=== Final Response ===")
    print(result["messages"][-1].content)
