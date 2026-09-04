from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL_NAME = "deepseek-r1:1.5b"


SYSTEM_PROMPT = """
You are PlacementPrep AI, an AI assistant created specifically
to help students prepare for job placements.

You can answer questions related to:

1. Python
2. Java
3. JavaScript
4. HTML and CSS
5. SQL
6. DBMS
7. Data Structures and Algorithms
8. Operating Systems
9. Computer Networks
10. Artificial Intelligence basics
11. Machine Learning basics
12. Technical interview preparation
13. HR interview preparation
14. Resume preparation
15. Placement preparation
16. Aptitude preparation

Rules:

- Give simple and easy-to-understand explanations.
- Use examples whenever useful.
- Help students prepare for interviews.
- If asked to explain a programming concept,
  provide a simple explanation and example.
- If asked an HR interview question,
  help the student create a good answer.
- If the user asks something completely unrelated
  to placement preparation, politely say:

  "I am PlacementPrep AI. I am designed to help with
  placement preparation, programming, technical interviews,
  HR interviews, aptitude, resumes, and related topics."

Do not pretend to have real-time information.
"""


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "PlacementPrep AI Backend is Running"
    })


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()


        if not data:

            return jsonify({
                "error": "No data received"
            }), 400


        user_message = data.get(
            "message",
            ""
        ).strip()


        if not user_message:

            return jsonify({
                "error": "Please enter a message"
            }), 400


        full_prompt = f"""
{SYSTEM_PROMPT}

User Question:
{user_message}

Assistant Answer:
"""


        payload = {

            "model": MODEL_NAME,

            "prompt": full_prompt,

            "stream": False

        }


        response = requests.post(

            OLLAMA_URL,

            json=payload,

            timeout=180

        )


        response.raise_for_status()


        result = response.json()


        bot_response = result.get(

            "response",

            "Sorry, I could not generate a response."

        )


        return jsonify({

            "response": bot_response

        })


    except requests.exceptions.ConnectionError:

        return jsonify({

            "error": "Cannot connect to Ollama. Please make sure Ollama is running."

        }), 500


    except requests.exceptions.Timeout:

        return jsonify({

            "error": "The AI model took too long to respond."

        }), 500


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )