import json
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

from app.db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route("/overview", methods=("GET",))
def overview():
    db = get_db()

    temperatures = db.execute("SELECT reading, created FROM temperature WHERE created >= datetime('now', '-24 hours') ORDER BY created ASC").fetchall()
    voltages = db.execute("SELECT reading, created FROM voltage WHERE created >= datetime('now', '-24 hours') ORDER BY created ASC").fetchall()

    temp_labels = json.dumps([row["created"].strftime("%H:%M") for row in temperatures])
    temp_values = json.dumps([row["reading"] for row in temperatures])
    volt_labels = json.dumps([row["created"].strftime("%H:%M") for row in voltages])
    volt_values = json.dumps([row["reading"] for row in voltages])

    return render_template("data/overview.html", temp_labels=temp_labels, temp_values=temp_values, volt_labels=volt_labels, volt_values=volt_values)

@bp.route("/manage", methods=("GET",))
def manage():
    db = get_db()

    temperatures = db.execute("SELECT id, reading, created FROM temperature WHERE created >= datetime('now', '-24 hours') ORDER BY created ASC").fetchall()
    voltages = db.execute("SELECT id, reading, created FROM voltage WHERE created >= datetime('now', '-24 hours') ORDER BY created ASC").fetchall()

    return render_template("data/manage.html", temperatures=temperatures, voltages=voltages)

@bp.route("/save", methods=("POST",))
def save():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid request"}), 400

    temperature = data.get("temperature")
    voltage = data.get("voltage")

    if temperature is None and voltage is None:
        return jsonify({"error": "Provide temperature and/or voltage"}), 400

    db = get_db()
    try:
        if temperature is not None:
            db.execute("INSERT INTO temperature (reading) VALUES (?)", (float(temperature),))

        if voltage is not None:
            db.execute("INSERT INTO voltage (reading) VALUES (?)", (float(voltage),))

        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return "", 200

@bp.route("/delete", methods=("POST",))
def delete():
    db = get_db()

    return 200

@bp.route("/clear", methods=("POST",))
def clear():
    db = get_db()

    return 200