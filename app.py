from flask import Flask, jsonify, render_template_string, session
import random

app = Flask(__name__)
app.secret_key = 'super-secret-key'

system_codes = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

@app.route('/status', methods=['GET'])
def get_status():
    damaged_system = random.choice(list(system_codes.keys()))
    session['damaged_system'] = damaged_system
    return jsonify({"damaged_system": damaged_system})

@app.route('/repair-bay', methods=['GET'])
def repair_bay():
    damaged_system = session.get('damaged_system')
    repair_code = system_codes.get(damaged_system, "UNKNOWN")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{repair_code}</div>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/teapot', methods=['POST'])
def teapot():
    return "I'm a teapot", 418

if __name__ == '__main__':
    app.run(debug=True)