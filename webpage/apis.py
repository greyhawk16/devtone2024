from flask import Flask, render_template, request, jsonify, json, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy

from webpage.app_tools import make_session_text, create_session, read_session, read_session_db
from webpage.app_tools import update_session_db, delete_session_db
from webpage.models import SessionDB
from webpage.app_class import Session, Problem, Check, Start, Gameover
from webpage import api_loaded_start, api_loaded_problem, api_loaded_result
import webpage.gpt as gpt

apis = Blueprint('apis', __name__)
app  = apis


@app.route('/loadingstart', methods=['POST'])
def loadingstart():
    token = request.form['token']
    return render_template("loadingstart.html", token=token)

@app.route('/loadingproblem', methods=['POST'])
def loadingproblem():
    token = request.form['token']
    return render_template("loadingproblem.html", token=token)

@app.route('/loadingresult', methods=['POST'])
def loadingresult():
    token = request.form['token']
    return render_template("loadingresult.html", token=token)

