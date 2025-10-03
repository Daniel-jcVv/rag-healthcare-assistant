from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from app.components.retriever import create_qa_chain
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom(24)

from markupsafe import Markup
def n12br(value):
    return Markup(value.replace('\n', '<br>'))

app.jinja_env.filters['n12br'] = n12br

@app.route('/', methods=['GET', 'POST'])
def index():
    if "messages" not in session:
        session["messages"] = []
    
    if request.method == 'POST':
        user_input = request.form.get("prompt")

        if user_input:
            messages = session["messages"]
            messages.append({"role": "user", "content": user_input})
            session["messages"] = messages

            try:
                qa_chain = create_qa_chain()
                response = qa_chain.invoke({"query" : user_input})
                result = response.get("result", "No response")

                messages.append({"role": "assistant", "content": result})
                session["messages"] = messages

            except Exception as e:
                error_msg = f"Error : {str(e)}"
                return render_template("index.html", messages = session["messages"], error=error_msg)
            
        return redirect(url_for("index"))
    return render_template("index.html", messages=session.get("messages", []))


@app.route("/clear")
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))


@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_question = data.get('question', '')

        if not user_question:
            return jsonify({
                'success': False,
                'error': 'No question provided'
            }), 400

        # Create QA chain and get response from Ollama
        qa_chain = create_qa_chain()
        response = qa_chain.invoke({"query": user_question})

        answer = response.get("result", "No response generated")
        source_documents = response.get("source_documents", [])

        # Format sources
        sources = []
        for doc in source_documents[:3]:  # Limit to top 3 sources
            sources.append({
                'document': doc.metadata.get('source', 'Unknown').split('/')[-1],  # Just filename
                'page': doc.metadata.get('page_label', doc.metadata.get('page', 'N/A'))
            })

        return jsonify({
            'success': True,
            'answer': answer,
            'sources': sources
        })

    except Exception as e:
        import traceback
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

