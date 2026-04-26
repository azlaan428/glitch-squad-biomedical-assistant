import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from agent.agent import build_agent

app = Flask(__name__)
agent_executor = None

def get_agent():
    global agent_executor
    if agent_executor is None:
        agent_executor = build_agent()
    return agent_executor

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "").strip()
    if not user_query:
        return jsonify({"error": "Empty query"}), 400
    try:
        agent = get_agent()
        result = agent.invoke({"messages": [{"role": "user", "content": user_query}]})
        response = result["messages"][-1].content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
