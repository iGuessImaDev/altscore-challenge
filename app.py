from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)
app.secret_key = 'super-secret-key'

SYSTEM_CODES = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

damaged_system = None  # memory between requests

@app.route('/status', methods=['GET'])
def status():
    global damaged_system
    damaged_system = random.choice(list(SYSTEM_CODES.keys()))
    return jsonify({"damaged_system": damaged_system})

@app.route('/repair-bay', methods=['GET'])
def repair_bay():
    global damaged_system
    code = SYSTEM_CODES.get(damaged_system, "UNKNOWN")
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{code}</div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/teapot', methods=['POST'])
def teapot():
    return "I'm a teapot", 418

if __name__ == '__main__':
    app.run(debug=True)