from flask import Flask, jsonify, render_template_string, request
import random

app = Flask(__name__)
app.secret_key = 'super-secret-key'

low_p = 0.05
high_p = 10
v_liquid_low = 0.00105
v_liquid_high = 0.0035
v_vapor_low = 0.03
v_vapor_high = 0.0035

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


@app.route('/phase-change-diagram', methods=['GET'])
def phase_change_diagram():
    try:
        pressure = float(request.args.get('pressure'))

        if pressure < low_p or pressure > high_p:
            return jsonify({"error": "Pressure out of range"}), 400

        # Linear interpolation for specific volume
        def lerp(p, p1, p2, v1, v2):
            return v1 + (p - p1) * (v2 - v1) / (p2 - p1)

        if pressure == high_p:
            v_liquid = v_liquid_high
            v_vapor = v_vapor_high
        else:
            v_liquid = lerp(pressure, low_p, high_p, v_liquid_low, v_liquid_high)
            v_vapor = lerp(pressure, low_p, high_p, v_vapor_low, v_vapor_high)

        return jsonify({
            "specific_volume_liquid": round(v_liquid, 6),
            "specific_volume_vapor": round(v_vapor, 6)
        })

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid pressure value"}), 400

if __name__ == '__main__':
    app.run(debug=True)