from flask import Flask, request, jsonify
from analyzer import analyze_business_idea

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    idea = data.get("idea", "")
    if not idea:
        return jsonify({"error": "Idea is required"}), 400

    result = analyze_business_idea(idea)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
