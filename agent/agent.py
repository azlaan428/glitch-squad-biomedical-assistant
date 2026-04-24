import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
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

REACT_PROMPT = PromptTemplate.from_template("""You are a biomedical research assistant. Use the tools available to answer the user's question accurately and concisely.

Tools available:
{tools}

Tool names: {tool_names}

Use EXACTLY this format:

Question: the input question you must answer
Thought: your reasoning about what to do
Action: the tool name to use (must be one of [{tool_names}])
Action Input: the input to the tool
Observation: the result of the tool
Thought: I now know the final answer
Final Answer: your comprehensive answer based on the literature

Begin!

Question: {input}
{agent_scratchpad}""")


def load_llm():
    from transformers import pipeline as hf_pipeline
    pipe = hf_pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device_map="auto",
        max_new_tokens=512,
    )
    return HuggingFacePipeline(pipeline=pipe)


def build_agent():
    llm = load_llm()
    tools = [pubmed_tool]
    agent = create_react_agent(llm, tools, REACT_PROMPT)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )


if __name__ == "__main__":
    print("Loading model... (cached, should be fast)")
    executor = build_agent()
    query = "What ML methods are used for epilepsy seizure detection?"
    print(f"\nQuery: {query}\n")
    response = executor.invoke({"input": query})
    print("\n=== Final Response ===")
    print(response["output"])
