from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.repo_utils import clone_repo
from utils.grader import grade_python, grade_java, grade_cpp
from utils.github_utils import get_last_commit_date
import os

app = Flask(__name__)
CORS(app)

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask backend!"})

@app.route("/api/submit-url", methods=["POST"])
def submit_url():
    data = request.get_json()
    url = data.get("url") if data else None
    test_cases = data.get("test_cases")
    language = data.get("language", "python")
    if not isinstance(test_cases, list):
        return jsonify({"message": "Test cases must be a list"}), 400
    if not url:
        return jsonify({"message": "No URL provided"}), 400

    repo_dir = "cloned_repo"
    try:
        clone_repo(url, repo_dir)
    except Exception as e:
        return jsonify({"message": f"Failed to clone repo: {str(e)}"}), 400

    main_py = os.path.join(repo_dir, "main.py")
    main_java = os.path.join(repo_dir, "Main.java")
    main_cpp = os.path.join(repo_dir, "main.cpp")

    try:
        if language == "python" and os.path.exists(main_py):
            results, total_points, earned_points = grade_python(main_py, test_cases)
            message = "Python test cases executed"
        elif language == "java" and os.path.exists(main_java):
            results, total_points, earned_points = grade_java(main_java, repo_dir, test_cases)
            message = "Java test cases executed"
        elif language == "cpp" and os.path.exists(main_cpp):
            results, total_points, earned_points = grade_cpp(main_cpp, repo_dir, test_cases)
            message = "C++ test cases executed"
        else:
            results = []
            total_points = 0
            earned_points = 0
            message = "main.py or Main.java not found in repo, or language not specified"
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    last_commit_date_str = get_last_commit_date(url)
    print(last_commit_date_str)

    report = {
        "message": message,
        "results": results,
        "score": {
            "earned_points": earned_points,
            "total_points": total_points,
            "percentage": round((earned_points / total_points) * 100, 2) if total_points else 0
        },
        "last_commit_date": last_commit_date_str
    }
    return jsonify(report), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)