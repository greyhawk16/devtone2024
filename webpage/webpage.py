from flask import Flask, render_template, request, jsonify, json, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy

from webpage.app_tools import make_session_text, create_session, read_session, read_session_db
from webpage.app_tools import update_session_db, delete_session_db
from webpage.models import SessionDB
from webpage.app_class import Session, Problem, Check, Start, Gameover
from webpage import api_loaded_start, api_loaded_problem, api_loaded_result


webpage = Blueprint('webpage', __name__)
app     = webpage

@app.route('/',      methods=['GET', 'POST'])
@app.route('/start', methods=['GET', 'POST'])
def start():
    return render_template("start.html", token=make_session_text())


@app.route('/problem', methods=['POST'])
def problem():
    token           = request.form['token']
    session         = read_session(token)
    problem_number  = str(session.problem_num)
    life            = str(session.life)
    image_url       = f"dataimg/img_{session.image_num}.png"
    description     = session.description
    option          = session.option
    
    return render_template("problem.html", problem_number=problem_number,
                           life=life, image_url=image_url, description=description,
                           option=option, token=token)


@app.route('/check', methods=['POST'])
def check():
    token           = request.form['token']
    result_all      = bool(request.form['lived'])
    session         = read_session(token)
    problem_number  = str(session.problem_num)
    life            = str(session.life)
    result_text     = session.result_text
    option          = session.option
    result          = session.result
    
    return render_template("check.html", problem_number=problem_number,
                           life=life, result_all=result_all, result_text=result_text,
                           option=option, result=result, token=token)


@app.route('/gameover', methods=['POST'])
def gameover():
    token           = make_session_text()
    problem_number  = request.form['problem_number']

    return render_template("gameover.html", token=token,
                           problem_number=problem_number)


@app.route('/loaded_start', methods=['POST'])
def loaded_start():
    token = request.form['token']
    if token not in api_loaded_start:
        return jsonify({
            "session": token,
            "result" : "false"
        })

    return jsonify(api_loaded_start[token])

@app.route('/loaded_problem', methods=['POST'])
def loaded_problem():
    token = request.form['token']
    if token not in api_loaded_start:
        return jsonify({
            "session": token,
            "result" : "false"
        })

    return jsonify(api_loaded_start[token])

@app.route('/loaded_result', methods=['POST'])
def loaded_result():
    token = request.form['token']
    if token not in api_loaded_start:
        return jsonify({
            "session": token,
            "result" : "false"
        })

    return jsonify(api_loaded_start[token])
