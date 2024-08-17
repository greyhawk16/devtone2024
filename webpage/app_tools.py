import random
from .app_class import Session
from . import db
from .models import SessionDB

session_length = 64

def make_session_text():
    database = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    while True:
        result = ''.join(random.choices(database, k=session_length))
        check  = SessionDB.query.filter_by(token=result).first()
        if not check:
            break
    
    return result

def create_session(token, problem_num=0, life=100,
                   description='', option=['','','',''],
                   result=[0,0,0,0], result_desc='',
                   image_num=0, conv_archive='') -> SessionDB:
    
    session = Session.create(
        token = token,
        problem_num = problem_num,
        life = life,
        description = description,
        option = option,
        result = result,
        result_desc = result_desc,
        conv_archive = conv_archive,
        image_num = image_num
        ).to_session_db()
    db.session.add(session)
    db.session.commit()
    
    return session

def read_session_db(token) -> SessionDB:
    session = SessionDB.query.filter_by(token=token).first()
    if not session:
        raise KeyError
    return session

def read_session(token) -> Session:
    session = read_session_db(token)
    return Session(session)

def update_session_db(token, **target) -> None:
    session = read_session_db(token)
    for tar in target:
        exec("session."+tar+"="+target[tar])
    db.session.add(session)
    db.session.commit()

def update_session_db_ses(sesorigin: Session) -> None:
    db.session.add(sesorigin.to_session_db())
    db.session.commit()

def delete_session_db(token) -> str:
    session = read_session_db(token)
    db.session.delete(session)
    db.session.commit()
    return token

def lose_life_calc(datalist, select):
    return datalist[select] - max(datalist)