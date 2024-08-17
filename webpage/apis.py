from flask import Flask, render_template, request, jsonify, json, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy

from webpage.app_tools import make_session_text, create_session, read_session, read_session_db
from webpage.app_tools import update_session_db, delete_session_db, lose_life_calc, update_session_db_ses
from webpage.models import SessionDB
from webpage.app_class import Problem, Check, Start, Gameover
from webpage import api_loaded_start, api_loaded_problem, api_loaded_result
import webpage.gpt as gpt
import threading
from . import db
from sqlalchemy.orm import scoped_session, sessionmaker, Session

apis = Blueprint('apis', __name__)
app  = apis

class StartWorker():
    def __init__(self, token):
        self.token = token

    def run(self):
        global api_loaded_start
        print("runned loaded start")
        session = create_session(token=self.token, problem_num=1, life=100)
        nextset = gpt.start_game(Problem(session)).to_session_db()

        update_session_db_ses(nextset)

        api_loaded_start[self.token] = {
            'session': self.token,
            'result':  "true",
	    }

        global api_loaded_problem
        global api_loaded_result

        try: del api_loaded_result[self.token]
        except: pass
        try: del api_loaded_problem[self.token]
        except: pass
        
class ProblemWorker():
    def __init__(self, token):
        self.token = token

    def run(self):
        global api_loaded_problem
        bef_session = read_session_db(token=self.token)

        session = create_session(token=make_session_text(),
                                 problem_num=bef_session.problem_num+1,
                                 life=bef_session.life)
        delete_session_db(bef_session)

        nextset = gpt.start_game(Problem(session)).to_session_db()

        update_session_db_ses(nextset)

        api_loaded_problem[self.token] = {
			'session': self.token,
		    'result': "true",
		    'next_session': nextset.token,
	    }
        
        global api_loaded_start
        global api_loaded_result
        
        try: del api_loaded_result[self.token]
        except: pass
        try: del api_loaded_start[self.token]
        except: pass
        
class ResultWorker():
    def __init__(self, token, select_number):
        self.token = token
        self.select_number = select_number

    def run(self):
        global api_loaded_result
        session = read_session_db(token=self.token)
        result  = gpt.get_input(Check(session, self.select_number))

        result.life -= lose_life_calc(result.result, self.select_number)

        if result.life <= 0:
            lived = 'false'
        else:
            lived = 'true'

        update_session_db_ses(result)
        
        api_loaded_result[self.token] = {
			'session': self.token,
		    'result': 'true',
		    'lived': lived
	    }
        
        global api_loaded_start
        global api_loaded_problem
        
        try: del api_loaded_result[self.token]
        except: pass
        try: del api_loaded_problem[self.token]
        except: pass

@app.route('/loadingstart', methods=['POST'])
def loadingstart():
    global api_loaded_start
    token = request.form['token']
    api_loaded_start[token] = {
            'session': token,
            'result':  "false",
	    }
    return render_template("loadingstart.html", token=token)

@app.route('/loadingproblem', methods=['POST'])
def loadingproblem():
    global api_loaded_problem
    token = request.form['token']
    api_loaded_problem[token] = {
			'session': token,
		    'result': "false",
		    'next_session': "",
	    }
    return render_template("loadingproblem.html", token=token)

@app.route('/loadingresult', methods=['POST'])
def loadingresult():
    global api_loaded_result
    
    token = request.form['token']
    select_number = request.form['select_number']
    api_loaded_result[token] = {
			'session': token,
		    'result': 'false',
		    'lived': 'true'
	    }
    return render_template("loadingresult.html", token=token)


@app.route('/loaded_start_action', methods=['POST'])
def loaded_start():
    token = request.json['token']
    StartWorker(token).run()
    return jsonify({"result": "true"})

@app.route('/loaded_problem_action', methods=['POST'])
def loaded_problem():
    token = request.json['token']
    ProblemWorker(token).run()
    return jsonify({"result": "true"})

@app.route('/loaded_result_action', methods=['POST'])
def loaded_result():
    token = request.json['token']
    select_number = request.json['select_number']
    ResultWorker(token, select_number).run()
    return jsonify({"result": "true"})
