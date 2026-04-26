import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
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

SYSTEM_PROMPT = """You are a biomedical research assistant. When given a question:
1. Use the PubMedSearch tool to retrieve relevant literature
2. Read the retrieved abstracts carefully
3. Answer the user's specific question directly based on what the abstracts say
4. Cite the PMID numbers of the papers you reference
5. Do not summarise unrelated papers — only answer what was asked"""

def build_agent():
    llm = ChatOllama(model="llama3.2", temperature=0)
    return create_react_agent(llm, [pubmed_tool], prompt=SYSTEM_PROMPT)

if __name__ == "__main__":
    print("Connecting to Ollama...")
    agent = build_agent()
    query = "What ML methods are used for epilepsy seizure detection?"
    print(f"\nQuery: {query}\n")
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("\n=== Final Response ===")
    print(result["messages"][-1].content)
