from flask import Flask, request, jsonify, send_from_directory
import subprocess, json, sys, os

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/<path:path>")
def frontend_files(path):
    return send_from_directory("frontend", path)


@app.route("/run", methods=["POST"])
def run():
    data   = request.get_json()
    result = subprocess.run([sys.executable, "backend/main.py"], input=json.dumps(data), capture_output=True, text=True)
    if not result.stdout.strip():
        return jsonify({"error": result.stderr or "No output", "prints": [], "graph1": "", "graph2": ""})
    return jsonify(json.loads(result.stdout))


@app.route("/game_setup", methods=["POST"])
def game_setup():
    body   = request.get_json()
    result = subprocess.run([sys.executable, "backend/game.py"], input=json.dumps({"mode": "setup", **body}), capture_output=True, text=True)
    if not result.stdout.strip():
        return jsonify({"error": result.stderr or "No output"})
    return jsonify(json.loads(result.stdout))


@app.route("/game_run", methods=["POST"])
def game_run():
    body   = request.get_json()
    result = subprocess.run([sys.executable, "backend/game.py"], input=json.dumps({"mode": "run", **body}), capture_output=True, text=True)
    if not result.stdout.strip():
        return jsonify({"error": result.stderr or "No output"})
    return jsonify(json.loads(result.stdout))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
