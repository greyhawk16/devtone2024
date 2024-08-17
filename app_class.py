from models import SessionDB


class Session():
    def __init__(self, SessionDB):
        self.token = SessionDB.token
        self.problem_number = int(SessionDB.problem_num)
        self.life = int(SessionDB.life)
        self.description = SessionDB.description
        self.option = [SessionDB.option1, SessionDB.option2, SessionDB.option3, SessionDB.option4]
        self.result = [int(SessionDB.result1), int(SessionDB.result2), int(SessionDB.result3), int(SessionDB.result4)]
        self.result_text = SessionDB.result_text

    @staticmethod
    def create(token, problem_number, life, description, option, result, result_text):
        return Session(
            token=token,
            problem_num=problem_number,
            life=life,
            description=description,
            option=[option[0], option[1], option[2], option[3]],
            result=[result[0], result[1], result[2], result[3]],
            result_text=result_text
        )

    def update(self, SessionDB):
        self.token = SessionDB.token
        self.problem_number = int(SessionDB.problem_num)
        self.life = int(SessionDB.life)
        self.description = SessionDB.description
        self.option = [SessionDB.option1, SessionDB.option2, SessionDB.option3, SessionDB.option4]
        self.result = [int(SessionDB.result1), int(SessionDB.result2), int(SessionDB.result3), int(SessionDB.result4)]
        self.result_text = SessionDB.result_text
    
    def to_session_db(self):
        return SessionDB(
            token=self.token,
            problem_num=self.problem_number,
            life=self.life,
            description=self.description,
            option1=self.option[0],
            option2=self.option[1],
            option3=self.option[2],
            option4=self.option[3],
            result1=self.result[0],
            result2=self.result[1],
            result3=self.result[2],
            result4=self.result[3],
            result_text=self.result_text
        )
    


class Problem():
    def __init__(self, Session, select_number):
        self.problem_number = Session.problem_number
        self.life = Session.life
        self.image_url = ""
        self.description = Session.description
        self.option = Session.option
        self.token = Session.token
        self.select_number = select_number

class Check():
    def __init__(self, Session):
        self.problem_number = Session.problem_number
        self.life = Session.life
        self.result_all = False
        self.result_text = Session.result_text
        self.option = Session.option
        self.token = Session.token
        self.option = Session.option
        self.result = Session.result

class Start():
    def __init__(self, Session):
        self.token = Session.token

class Gameover():
    def __init__(self, Session):
        self.token = Session.token
        self.result_text = Session.result_text