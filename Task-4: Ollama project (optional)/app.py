from flask import Flask, render_template, request, jsonify
import ollama
import PyPDF2

app = Flask(__name__)


def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return str(e)


def clean_response(response):
    """Clean the LLM response to remove common prefixes and formatting"""
    text = response.strip()
    # Remove common prefixes
    prefixes = [
        "Here are the flash cards:",
        "Here's your response:",
        "Here are your flash cards:",
        "Flash cards:",
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix) :].strip()
    return text


def generate_flashcards(content, topic):
    """Generate flash cards using Ollama"""
    prompt = f"""
    Create concise and effective flash cards from the following study material about {topic}.
    
    Study Material:
    {content}

    Instructions:
    1. Create flash cards in this exact format (maintain the exact markdown format):
    Q: [Question]
    A: [Clear, concise answer]
    ---
    
    2. Guidelines for creating flash cards:
    - Create 5-7 flash cards
    - Questions should test understanding, not just memorization
    - Answers should be clear and straight to the point
    - Cover the most important concepts from the material
    - Avoid yes/no questions
    - Each answer should be 1-3 lines maximum
    
    Generate only the flash cards with no additional text or explanations.
    """

    try:
        response = ollama.chat(
            model="llama3.2", messages=[{"role": "user", "content": prompt}]
        )

        return clean_response(response["message"]["content"])
    except Exception as e:
        return f"Error generating flash cards: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if "notes_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["notes_file"]
    topic = request.form.get("topic", "this subject")

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a PDF file"}), 400

    try:
        content = extract_text_from_pdf(file)
        flashcards_text = generate_flashcards(content, topic)

        # Parse flashcards into structured format
        flashcards = []
        cards = flashcards_text.split("---")

        for card in cards:
            card = card.strip()
            if not card:
                continue

            parts = card.split("A:")
            if len(parts) != 2:
                continue

            question = parts[0].replace("Q:", "").strip()
            answer = parts[1].strip()

            flashcards.append({"question": question, "answer": answer})

        return jsonify({"flashcards": flashcards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
