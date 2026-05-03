import sys, os, json, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, render_template, request, jsonify, send_file, Response, stream_with_context
from agent.agent import (run_pipeline, run_query_architect, run_literature_scout,
                         run_evidence_synthesiser, run_citation_builder, llm_invoke_with_retry)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT
import io

app = Flask(__name__)


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
        result = run_pipeline(user_query)
        return jsonify({
            "synthesis": result["synthesis"],
            "citations": result["citations"],
            "paper_count": result["paper_count"],
            "queries": result["queries"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stream", methods=["GET"])
def stream():
    user_query = request.args.get("query", "").strip()
    if not user_query:
        return jsonify({"error": "Empty query"}), 400

    def generate():
        def emit(event, data):
            return "event: " + event + "\ndata: " + json.dumps(data) + "\n\n"

        try:
            # Stage 1
            yield emit("stage", {"stage": 1, "pct": 10})
            queries = run_query_architect(user_query)
            yield emit("queries", {"queries": queries, "pct": 25})

            # Stage 2
            yield emit("stage", {"stage": 2, "pct": 35})
            papers = run_literature_scout(queries)
            yield emit("papers", {"paper_count": len(papers), "pct": 50})

            # PRISMA filter
            yield emit("stage", {"stage": 3, "pct": 55})
            from agent.agent import run_prisma_filter
            filtered = run_prisma_filter(user_query, papers)
            included = {pmid: p for pmid, p in filtered.items() if p["included"]}
            yield emit("prisma", {
                "filtered": {
                    pmid: {"title": p.get("title", ""), "included": p["included"], "reason": p["reason"]}
                    for pmid, p in filtered.items()
                },
                "included_count": len(included),
                "excluded_count": len(filtered) - len(included),
                "pct": 65
            })
            time.sleep(12)

            # Stage 4 - synthesise on included papers only
            yield emit("stage", {"stage": 4, "pct": 70})
            synthesis = run_evidence_synthesiser(user_query, included)
            yield emit("synthesis", {"synthesis": synthesis, "pct": 88})

            # Stage 5
            yield emit("stage", {"stage": 5, "pct": 90})
            citations = run_citation_builder(included)
            yield emit("done", {
                "synthesis": synthesis,
                "citations": citations,
                "paper_count": len(included),
                "queries": queries,
                "papers": {
                    pmid: {
                        "title": p.get("title", ""),
                        "abstract": p.get("abstract", ""),
                        "authors": p.get("authors", ""),
                        "journal": p.get("journal", ""),
                        "year": p.get("year", "")
                    } for pmid, p in included.items()
                },
                "pct": 100
            })

        except Exception as e:
            yield emit("error", {"message": str(e)})

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.route("/export-pdf", methods=["POST"])
def export_pdf():
    data = request.get_json()
    synthesis = data.get("synthesis", "")
    citations = data.get("citations", "")
    query = data.get("query", "Biomedical Research Query")
    paper_count = data.get("paper_count", 0)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm)

    accent = colors.HexColor("#00e5a0")
    dark = colors.HexColor("#111827")

    title_style = ParagraphStyle("title",
        fontName="Helvetica-Bold", fontSize=18,
        textColor=dark, spaceAfter=4)
    meta_style = ParagraphStyle("meta",
        fontName="Helvetica", fontSize=9,
        textColor=colors.HexColor("#5a6a7a"), spaceAfter=16)
    section_label_style = ParagraphStyle("sec_label",
        fontName="Helvetica-Bold", fontSize=10,
        textColor=accent, spaceBefore=14, spaceAfter=4)
    body_style = ParagraphStyle("body",
        fontName="Helvetica", fontSize=10,
        leading=16, textColor=dark, spaceAfter=6)
    cite_style = ParagraphStyle("cite",
        fontName="Helvetica", fontSize=8,
        leading=13, textColor=colors.HexColor("#444444"),
        spaceAfter=4)

    story = []
    story.append(Paragraph("ARIA — Autonomous Research Intelligence Agent", title_style))
    story.append(Paragraph(
        "Query: " + query + "  |  " + str(paper_count) + " papers retrieved  |  Groq LLaMA-3.1",
        meta_style))
    story.append(HRFlowable(width="100%", thickness=1,
        color=colors.HexColor("#1e2936"), spaceAfter=16))

    SECTIONS = [
        ("## Background", "Background"),
        ("## Key Findings", "Key Findings"),
        ("## Level of Evidence", "Level of Evidence"),
        ("## Conflicting Evidence", "Conflicting Evidence"),
        ("## Research Gaps", "Research Gaps"),
        ("## Clinical Implications", "Clinical Implications"),
    ]
    for marker, label in SECTIONS:
        start = synthesis.find(marker)
        if start == -1:
            continue
        content_start = start + len(marker)
        next_markers = [synthesis.find(m) for m, _ in SECTIONS if synthesis.find(m) > start]
        end = min(next_markers) if next_markers else len(synthesis)
        text = synthesis[content_start:end].strip()
        if not text:
            continue
        story.append(Paragraph(label.upper(), section_label_style))
        for para in text.split("\n"):
            para = para.strip()
            if para:
                story.append(Paragraph(para, body_style))

    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=1,
        color=colors.HexColor("#1e2936"), spaceAfter=8))
    story.append(Paragraph("REFERENCES", section_label_style))
    for line in citations.split("\n"):
        line = line.strip()
        if line:
            story.append(Paragraph(line, cite_style))

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "AI-generated synthesis — verify against primary sources before clinical use.",
        ParagraphStyle("disclaimer", fontName="Helvetica-Oblique",
            fontSize=8, textColor=colors.HexColor("#999999"))))

    doc.build(story)
    buf.seek(0)
    safe_query = "".join(c for c in query[:40] if c.isalnum() or c in " -_").strip()
    filename = "ARIA_" + safe_query.replace(" ", "_") + ".pdf"
    return send_file(buf, mimetype="application/pdf",
        as_attachment=True, download_name=filename)


@app.route("/score", methods=["POST"])
def score():
    data = request.get_json()
    synthesis = data.get("synthesis", "")
    if not synthesis:
        return jsonify({"error": "No synthesis provided"}), 400
    try:
        from agent.agent import run_confidence_scorer
        scores = run_confidence_scorer(synthesis)
        return jsonify({"scores": scores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/selective-review", methods=["POST"])
def selective_review():
    data = request.get_json()
    question = data.get("question", "")
    selected_papers = data.get("papers", {})
    if not selected_papers:
        return jsonify({"error": "No papers selected"}), 400
    try:
        from agent.agent import run_selective_review
        review = run_selective_review(question, selected_papers)
        return jsonify({"review": review})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    question = data.get("question", "")
    synthesis = data.get("synthesis", "")
    if not synthesis:
        return jsonify({"error": "No synthesis provided"}), 400
    try:
        from agent.agent import run_predictive_model
        prediction = run_predictive_model(question, synthesis)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


import json as _json
from datetime import datetime
SESSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sessions.json")


def load_sessions():
    try:
        return _json.load(open(SESSIONS_FILE))
    except:
        return []


def save_session(entry):
    sessions = load_sessions()
    sessions.insert(0, entry)
    sessions = sessions[:20]
    _json.dump(sessions, open(SESSIONS_FILE, "w"), indent=2)


@app.route("/sessions", methods=["GET"])
def get_sessions():
    return jsonify({"sessions": load_sessions()})


@app.route("/sessions/save", methods=["POST"])
def save_session_route():
    data = request.get_json()
    save_session({
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "timestamp": datetime.now().strftime("%b %d, %H:%M"),
        "query": data.get("query", ""),
        "synthesis": data.get("synthesis", ""),
        "citations": data.get("citations", ""),
        "paper_count": data.get("paper_count", 0),
        "queries": data.get("queries", []),
        "papers": data.get("papers", {})
    })
    return jsonify({"ok": True})


@app.route("/extract-table", methods=["POST"])
def extract_table():
    data = request.get_json()
    question = data.get("question", "")
    synthesis = data.get("synthesis", "")
    papers = data.get("papers", {})
    if not synthesis:
        return jsonify({"error": "No synthesis provided"}), 400
    try:
        from agent.agent import run_table_extractor
        table = run_table_extractor(question, synthesis, papers)
        return jsonify({"table": table})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/followup", methods=["POST"])
def followup():
    data = request.get_json()
    question = data.get("question", "")
    original_question = data.get("original_question", "")
    synthesis = data.get("synthesis", "")
    papers = data.get("papers", {})
    if not question or not synthesis:
        return jsonify({"error": "Missing question or synthesis"}), 400
    try:
        from agent.agent import get_llm
        llm = get_llm()
        corpus = "\n\n".join(
            f"[PMID {pmid}] {p.get('title','')}\n{p.get('abstract','')[:300]}"
            for pmid, p in list(papers.items())[:6]
        )
        prompt = (
            f"You are a biomedical research assistant. The user previously asked:\n"
            f"\"{original_question}\"\n\n"
            f"Based on this evidence synthesis and retrieved papers, answer their follow-up question.\n"
            f"Be concise and cite PMIDs where relevant.\n\n"
            f"Synthesis:\n{synthesis[:1500]}\n\n"
            f"Papers:\n{corpus}\n\n"
            f"Follow-up Question: {question}"
        )
        response = llm_invoke_with_retry(llm, prompt)
        return jsonify({"answer": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)