from flask import Flask, request, jsonify, render_template_string

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
    html = """
    <!DOCTYPE html>
    <html lang="fa">
    <head>
      <meta charset="UTF-8" />
      <title>ESP Dashboard</title>
      <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; }
        h1 { margin-bottom: 8px; }
        .value { font-size: 2rem; color: #222; }
        .hint { margin-top: 24px; color: #666; font-size: 0.95rem; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }
      </style>
    </head>
    <body>
      <h1>آخرین عدد دریافتی</h1>
      <div class="value">{{ value }}</div>

      <div class="hint">
        برای ارسال عدد از ESP یا Postman به این مسیر POST بزنید:
        <br />
        <code>/number</code>
        با بدنه‌ی JSON مثلاً:
        <code>{"value": 123}</code>
        <br />
        برای دریافت JSON به‌روز از:
        <code>/latest</code>
        استفاده کنید.
      </div>
    </body>
    </html>
    """
    return render_template_string(html, value=latest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
