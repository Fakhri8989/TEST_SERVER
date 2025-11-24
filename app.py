from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
numbers = []

@app.route('/')
def home():
    return "ESP Number Server is running!"

@app.route('/number', methods=['POST'])
def receive_number():
    data = request.get_json()
    num = data.get('value') if data else None
    if num is not None:
        numbers.append(num)
        return jsonify({"status": "received", "value": num}), 200
    else:
        return jsonify({"error": "No value provided"}), 400

@app.route('/latest')
def latest_number():
    if numbers:
        return jsonify({"latest_value": numbers[-1]})
    else:
        return jsonify({"message": "No data yet"})

@app.route('/dashboard')
def dashboard():
    latest = numbers[-1] if numbers else "No data yet"
    return render_template("dashboard.html", value=latest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
